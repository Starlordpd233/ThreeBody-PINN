# Phase 5 — Verification + Final Cutover Cleanup

## Goal
Verify functional correctness across all variants, ensure no stale path refs remain, then remove old tree/rules safely.

## 5.1 Search for stale `3_Body_Problem` references
```bash
cd <home>/Desktop/cursor
rg "3_Body_Problem" --type py --type tex --type md --type txt -l \
  --glob '!brutus_simulation_documentation/*' \
  --glob '!docs/plans/*' \
  --glob '!.git/*'
```

Expected: no actionable references in active code/docs.

**Note:** `docs/plans/` is excluded because the phase plan documents intentionally contain `3_Body_Problem` references as part of their old→new change tables. `brutus_simulation_documentation/` is excluded because it contains historical terminal logs.

## 5.2 Validate dataset checks for all 4 variants

**Prerequisite:** Phase 1 Steps 8-10 must be applied first — they fix the `--modules` propagation bug, metrics filename pattern, and metrics JSON key schema. Without those fixes, `--modules correspondence` would silently run all modules, and metrics validation would fail on filename/key mismatches.

```bash
cd <home>/Desktop/cursor
for variant in hierarchical hierarchical_gold standard standard_gold; do
  PYTHONPATH="simulation_data" python3 -m Validation.dataset_readiness_checks \
    --variants "$variant" \
    --modules correspondence \
    --output-dir "/tmp/restructure_verification/$variant"
done
```

If module import fails with `ModuleNotFoundError: No module named 'Validation'`, verify that Phase 3 created the namespace marker:
```bash
test -f simulation_data/Validation/__init__.py && echo "OK: __init__.py exists" || echo "MISSING: create it with: touch simulation_data/Validation/__init__.py"
```

## 5.3 Validate parser classification for standard files
```bash
cd <home>/Desktop/cursor
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, 'pinn/data-handling/core')
from parsing import detect_simulation_metadata
pairs = [
  (
    Path('simulation_data/Data/ic_final/ic_standard_quasi_random/ic_standard_0000.txt'),
    Path('simulation_data/Data/brutus_output/brutus_standard_quasi_random/brutus_standard_0000.txt')
  ),
  (
    Path('simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard/ic_standard_gold_0000.txt'),
    Path('simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_gold_0000.txt')
  ),
]
for ic, br in pairs:
    if ic.exists() and br.exists():
        meta = detect_simulation_metadata(ic, br)
        print(f'OK: {ic.name} -> dataset_type={meta.dataset_type}, set_name={meta.set_name}')
    else:
        print(f'SKIP: missing {ic} or {br}')
"
```

## 5.4 Confirm ignored data remains ignored
```bash
cd <home>/Desktop/cursor
git status --short | rg "simulation_data/Data/|simulation_data/Validation/prescreening/prescreening_data/|simulation_data/Validation/analysis/figures/" || true
```

## 5.5 Cleanup old artifacts safely
```bash
cd <home>/Desktop/cursor
rm -rf "3_Body_Problem/brutus_metrics/backup data/"
rm -f 3_Body_Problem/brutus_progress.json
find 3_Body_Problem -type d -name "__pycache__" -exec rm -rf {} +
find 3_Body_Problem -type d -empty -delete
```

Delete old root only if no files remain:
```bash
if [ -d 3_Body_Problem ]; then
  remaining=$(find 3_Body_Problem -type f | wc -l)
  if [ "$remaining" -eq 0 ]; then
    rmdir 3_Body_Problem
  else
    echo "ERROR: 3_Body_Problem still has $remaining files" >&2
    find 3_Body_Problem -type f | head -40
    exit 1
  fi
fi
```

## 5.6 Pattern-based `.gitignore` cleanup (no fixed line numbers)

After old tree removal:
```bash
cd <home>/Desktop/cursor
sed -i '' '/^3_Body_Problem\//d' .gitignore
```

(Optional) remove now-empty legacy comment block manually if desired.

Commit final cleanup:
```bash
git add -A
git commit -m "chore: finalize simulation_data cutover and remove legacy 3_Body_Problem ignore rules"
```

## Exit Criteria
- Verification succeeds across all variants.
- No active stale path references.
- Old `3_Body_Problem` tree removed or explicitly blocked with diagnostics.
- `.gitignore` no longer contains `3_Body_Problem/...` rules.
