#!/usr/bin/env python3
"""Script para ejecutar backup si ha pasado suficiente tiempo según la configuración.

Uso: ejecutar diariamente desde cron; el script decidirá si crear copia según `backup_config.json`.
"""
import os
import json
import subprocess
import shutil
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from sqlalchemy import func
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT, 'backup_config.json')
BACKUPS_DIR = os.path.join(ROOT, 'backups')

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

def read_config():
    """Read the schedule written by the API, falling back to the default."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f) or {}
    except Exception:
        pass
    return {}

def last_backup_time():
    if not os.path.exists(BACKUPS_DIR):
        return None
    files = []
    for filename in os.listdir(BACKUPS_DIR):
        if not filename.startswith('backup_'):
            continue
        path = os.path.join(BACKUPS_DIR, filename)
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            continue
        # Do not let marker files written by an older failed implementation
        # postpone a real automatic backup.
        with open(path, 'rb') as backup_file:
            if backup_file.read(32).startswith(b'Fallback backup created'):
                continue
        files.append(path)
    if not files:
        return None
    latest = max(files, key=os.path.getmtime)
    # Keep this timezone-aware: `now` below is UTC-aware as well.
    return datetime.fromtimestamp(os.path.getmtime(latest), tz=timezone.utc)

def ensure_backups_dir():
    os.makedirs(BACKUPS_DIR, exist_ok=True)

def perform_backup(outfile):
    """Create a restorable database snapshot.

    A backup must never silently degrade to a text marker: callers only add it
    to the history when the database dump itself succeeds.
    """
    database_url = os.getenv('DATABASE_URL')
    # If DATABASE_URL not set in environment (e.g., running locally), try importing
    # the constructed URL from backend.database to keep behavior consistent.
    if not database_url:
        try:
            from database import DATABASE_URL as DATABASE_URL_CONF
            database_url = DATABASE_URL_CONF
        except Exception:
            database_url = None
    if database_url and 'postgres' in database_url:
        # Prefer an explicit PG_DUMP_PATH, fall back to PATH lookup (pg_dump or pg_dump.exe)
        pg_dump_path = os.getenv('PG_DUMP_PATH') or shutil.which('pg_dump') or shutil.which('pg_dump.exe')
        if not pg_dump_path:
            print('pg_dump not found: set PG_DUMP_PATH or install pg_dump in PATH')
            return False
        try:
            print('Creating PostgreSQL dump using', pg_dump_path)
            subprocess.check_call([
                pg_dump_path, '--dbname', database_url,
                '--format=plain', '--no-owner', '--no-privileges',
                '--file', outfile,
            ])
            return True
        except Exception as e:
            print('pg_dump failed:', e)
            return False

    # If sqlite, copy file
    if database_url and database_url.startswith('sqlite'):
        # sqlite:///./db.sqlite -> extract path
        path = database_url.replace('sqlite:///', '')
        if os.path.exists(path):
            shutil.copy2(path, outfile)
            return True

    print('No supported database source was found; backup not created.')
    return False


def append_log(entry: dict):
    log_path = os.path.join(ROOT, 'backup_log.json')
    data = []
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                data = json.load(f) or []
    except Exception:
        data = []

    data.append(entry)
    temp_path = f'{log_path}.tmp'
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, default=str, indent=2, ensure_ascii=False)
        os.replace(temp_path, log_path)
    except Exception as exc:
        print(f'Could not update backup log: {exc}', file=sys.stderr)
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass

def current_balance():
    """Return the balance represented by paid transactions at backup time."""
    try:
        from database import SessionLocal
        import models

        db = SessionLocal()
        try:
            total_income = db.query(func.coalesce(func.sum(models.Transaction.amount), 0)).filter(
                models.Transaction.type == models.TransactionType.income,
                models.Transaction.user_id == 1,
                models.Transaction.is_paid == True,
            ).scalar()
            total_expense = db.query(func.coalesce(func.sum(models.Transaction.amount), 0)).filter(
                models.Transaction.type == models.TransactionType.expense,
                models.Transaction.user_id == 1,
                models.Transaction.is_paid == True,
            ).scalar()
            total_invest = db.query(func.coalesce(func.sum(models.Transaction.amount), 0)).filter(
                models.Transaction.type == models.TransactionType.invest,
                models.Transaction.user_id == 1,
                models.Transaction.is_paid == True,
            ).scalar()
            return float((total_income or 0) - (total_expense or 0) - (total_invest or 0))
        finally:
            db.close()
    except Exception:
        return None


def main(force=False):
    cfg = read_config()
    freq_days = int(cfg.get('frequency_days', 7))

    lb = last_backup_time()
    now = datetime.now(timezone.utc)

    if force or lb is None or (now - lb) >= timedelta(days=freq_days):
        ensure_backups_dir()
        ts = now.strftime('%Y%m%d_%H%M%S')
        # Use .sql for SQL dumps; if backing up sqlite file we still keep .sql to maintain history
        outfile = os.path.join(BACKUPS_DIR, f'backup_{ts}.sql')
        print('Creating backup to', outfile)
        ok = perform_backup(outfile)
        if ok:
            print('Backup created:', outfile)
            entry = {
                'timestamp': now.isoformat(),
                'file': os.path.basename(outfile),
                'absolute_path': os.path.abspath(outfile),
                'balance': current_balance(),
            }
            append_log(entry)
        else:
            # A failed pg_dump can leave an empty or partial file behind. It
            # must not be considered the last backup on the next run.
            try:
                if os.path.exists(outfile):
                    os.remove(outfile)
            except OSError as exc:
                print(f'Could not remove failed backup: {exc}', file=sys.stderr)
            print('Backup failed')
            return False
    else:
        print('No backup needed. Last backup at', lb.isoformat())
    return True

if __name__ == '__main__':
    sys.exit(0 if main(force='--force' in sys.argv) else 1)
