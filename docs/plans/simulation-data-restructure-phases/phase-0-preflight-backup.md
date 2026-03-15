# Phase 0 — Preflight + Backup (Mandatory)

## Goal
Create a reproducible rollback point for both tracked and gitignored data before any migration.

## Steps

### 0.1 Ensure repository root and clean state
```bash
cd <home>/Desktop/cursor
git status --short
```

If dirty, either:
- commit your current work intentionally, or
- stop and defer migration

Do **not** auto-commit blindly.

### 0.2 Create tracked snapshot tag (no redundant commit)
```bash
if git rev-parse pre-restructuring-snapshot >/dev/null 2>&1; then
  echo "Tag pre-restructuring-snapshot already exists; leaving it unchanged"
else
  git tag pre-restructuring-snapshot
fi
git show --no-patch --oneline pre-restructuring-snapshot
```

### 0.3 Verify disk space before filesystem backup
```bash
src="3_Body_Problem"
dst="../3_Body_Problem_backup"
required_kb=$(du -sk "$src" | awk '{print $1}')
avail_kb=$(df -Pk .. | awk 'NR==2 {print $4}')
printf "required=%sKB available=%sKB\n" "$required_kb" "$avail_kb"
if [ "$avail_kb" -lt "$required_kb" ]; then
  echo "ERROR: insufficient disk space for backup" >&2
  exit 1
fi
```

### 0.4 Create filesystem backup for gitignored data
```bash
rsync -a --delete --info=progress2 3_Body_Problem/ ../3_Body_Problem_backup/
ls ../3_Body_Problem_backup | head -20
du -sh ../3_Body_Problem_backup
```

### 0.5 Record quick parity checks
```bash
echo "src files:  $(find 3_Body_Problem -type f | wc -l)"
echo "backup files: $(find ../3_Body_Problem_backup -type f | wc -l)"
```

## Exit Criteria
- `pre-restructuring-snapshot` tag exists.
- `../3_Body_Problem_backup/` exists and has comparable file counts.
- No migration has started yet.

## Rollback
- Tracked: `git reset --hard pre-restructuring-snapshot`
- Gitignored data: `rsync -a --delete ../3_Body_Problem_backup/ 3_Body_Problem/`
