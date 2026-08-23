#!/usr/bin/env bash
set -euo pipefail

# Run inside the Compose backend container so it uses its DATABASE_URL and
# pg_dump installation. Backups stay in the mounted ./backend/backups folder.
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CRON_ENTRY="0 3 * * * cd $PROJECT_ROOT && /usr/bin/docker compose exec -T backend python3 scripts/run_backup_if_needed.py >> $PROJECT_ROOT/backend/backup.log 2>&1"

# Check if already installed
crontab -l 2>/dev/null | grep -F "$CRON_ENTRY" >/dev/null 2>&1 && echo "Cron entry already installed" && exit 0

(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
echo "Cron entry installed"
