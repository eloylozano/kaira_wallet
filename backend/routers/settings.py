from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
import os
import json
from database import get_db
import models
from datetime import datetime
from fastapi.responses import FileResponse

router = APIRouter(tags=["Settings"])

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backup_config.json')


def _write_config_file(data: dict):
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass


@router.get('/backup')
def get_backup_config(db: Session = Depends(get_db)):
    row = db.query(models.BackupSetting).first()
    if not row:
        return {"frequency_days": None}
    return {"frequency_days": row.frequency_days, "last_updated": row.updated_at.isoformat() if row.updated_at else None}


@router.post('/backup')
def set_backup_config(payload: dict = Body(...), db: Session = Depends(get_db)):
    freq = payload.get('frequency_days')
    if freq is None:
        raise HTTPException(status_code=400, detail='frequency_days required')

    try:
        freq = int(freq)
    except Exception:
        raise HTTPException(status_code=400, detail='frequency_days must be integer')

    row = db.query(models.BackupSetting).first()
    if not row:
        row = models.BackupSetting(frequency_days=freq)
        db.add(row)
    else:
        row.frequency_days = freq
        row.updated_at = datetime.utcnow()

    db.commit()

    result = {"frequency_days": row.frequency_days, "last_updated": row.updated_at.isoformat() if row.updated_at else None}
    # write config file for compatibility with script
    _write_config_file(result)
    return result


@router.get('/backup/logs')
def get_backup_logs():
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backup_log.json')
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, 'r') as f:
            logs = json.load(f) or []
            # Older entries stored "backups/<file>". Keep the public API and
            # download endpoint independent from the storage path.
            visible_logs = []
            backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
            for entry in logs:
                filename = os.path.basename(entry.get("file", ""))
                path = os.path.join(backup_dir, filename)
                if not filename or not os.path.isfile(path):
                    continue
                # Previous versions produced a small marker file after a
                # failed dump. Do not present that as a successful backup.
                with open(path, "rb") as backup_file:
                    if backup_file.read(32).startswith(b"Fallback backup created"):
                        continue
                visible_logs.append({
                    "timestamp": entry.get("timestamp"),
                    "file": filename,
                    "balance": entry.get("balance"),
                })
            return visible_logs
    except Exception:
        return []


@router.get('/backup/download')
def download_backup(file: str):
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
    # sanitize: only allow filenames without path
    if '..' in file or '/' in file or '\\' in file:
        raise HTTPException(status_code=400, detail='Invalid file')
    path = os.path.join(base, file)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='Not found')
    return FileResponse(path, media_type='application/octet-stream', filename=file)


@router.post('/backup/run')
def run_backup_now(db: Session = Depends(get_db)):
    """Trigger the backup script immediately and return its output/status."""
    import subprocess
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'run_backup_if_needed.py')
    if not os.path.exists(script):
        raise HTTPException(status_code=500, detail='Backup script not found')

    try:
        completed = subprocess.run(
            ["/usr/bin/env", "python3", script, "--force"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True,
            timeout=120,
        )
        ok = completed.returncode == 0
        return {
            'ok': ok,
            'returncode': completed.returncode,
            'stdout': completed.stdout,
            'stderr': completed.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
