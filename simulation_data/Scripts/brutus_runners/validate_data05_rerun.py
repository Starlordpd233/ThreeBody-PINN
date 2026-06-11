import os
import sys
import json
import hashlib
import pathlib

IDS = [f"{i:04d}" for i in range(5, 60)] + [f"{i:04d}" for i in range(61, 76)]

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent
PROBES_OUT_DIR = REPO_ROOT / ".planning" / "phases" / "24-empirical-dataset-verification-and-correction-addendum" / "probes" / "outputs"
OLD_OUTPUT_DIR = REPO_ROOT / "simulation_data" / "Data" / "brutus_output" / "brutus_hierarchical"
STAGING_DIR = REPO_ROOT / "simulation_data" / "Data" / "rerun_staging" / "data05_gap24-01"
IC_DIR = REPO_ROOT / "simulation_data" / "Data" / "ic_final" / "ic_hierarchical"

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    PROBES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Gate 1: SHA256 of 70 old files
    hash_manifest_path = PROBES_OUT_DIR / "data05_old70_sha256.txt"
    with open(hash_manifest_path, 'w') as f:
        for id_str in IDS:
            old_file = OLD_OUTPUT_DIR / f"brutus_hierarchical_{id_str}.txt"
            if old_file.exists():
                f.write(f"{get_sha256(old_file)}  brutus_hierarchical_{id_str}.txt\n")
            else:
                f.write(f"MISSING  brutus_hierarchical_{id_str}.txt\n")
    print(f"Gate 1: Generated old file hash manifest at {hash_manifest_path.relative_to(REPO_ROOT)}")

    # Validation
    report = {
        'total': len(IDS),
        'missing': 0,
        'passes': 0,
        'failures': 0,
        'details': {}
    }
    
    for id_str in IDS:
        staged_file = STAGING_DIR / f"brutus_hierarchical_{id_str}.txt"
        ic_file = IC_DIR / f"ic_hierarchical_{id_str}.txt"
        
        detail = {'id': id_str, 'status': 'pass', 'errors': []}
        
        if not staged_file.exists():
            detail['status'] = 'fail'
            detail['errors'].append('Staged file missing')
            report['missing'] += 1
            report['failures'] += 1
            report['details'][id_str] = detail
            continue
            
        # Parse IC
        ic_lines = []
        with open(ic_file) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 7:
                    ic_lines.append([float(x) for x in parts])
        
        # Parse Output
        with open(staged_file) as f:
            content = f.read()
            
        lines = content.strip().split('\n')
        
        snapshots = []
        current_snap = None
        
        i = 0
        footer_found = False
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            parts = line.split()
            if len(parts) == 3 and parts[1] == '3': # Header: t N t_cpu (t=0 prints without decimal point)
                current_snap = {'t': float(parts[0]), 'N': int(parts[1]), 't_cpu': float(parts[2]), 'bodies': []}
                for j in range(3):
                    i += 1
                    if i >= len(lines): break
                    body_parts = lines[i].strip().split()
                    if len(body_parts) == 7:
                        current_snap['bodies'].append([float(x) for x in body_parts])
                    else:
                        detail['errors'].append(f'Invalid body line length {len(body_parts)} at snapshot {len(snapshots)}')
                snapshots.append(current_snap)
            elif 'Result' in line or 't_cpu' in line:
                footer_found = True
            i += 1
            
        if not snapshots:
            detail['errors'].append('No valid snapshots found')
            detail['status'] = 'fail'
            report['failures'] += 1
            report['details'][id_str] = detail
            continue

        # Gate 3: First snapshot masses == IC masses
        snap0 = snapshots[0]
        for b_idx in range(3):
            if snap0['bodies'][b_idx][0] != ic_lines[b_idx][0]:
                detail['errors'].append(f'Mass mismatch at t=0 for body {b_idx}: {snap0["bodies"][b_idx][0]} != {ic_lines[b_idx][0]}')
        
        # Informational: pos/vel match
        for b_idx in range(3):
            for k in range(1, 7):
                if snap0['bodies'][b_idx][k] != ic_lines[b_idx][k]:
                    detail['errors'].append(f'Pos/Vel mismatch at t=0 for body {b_idx} param {k}: {snap0["bodies"][b_idx][k]} != {ic_lines[b_idx][k]}')

        # Gate 4: Final snapshot time == 10.0, count == 126
        if len(snapshots) != 126:
            detail['errors'].append(f'Snapshot count {len(snapshots)} != 126')
        
        final_t = snapshots[-1]['t']
        if final_t < 9.5 or abs(final_t - 10.0) > 0.08:
            detail['errors'].append(f'Final t {final_t} out of bounds')
        detail['final_t'] = final_t
        detail['footer_found'] = footer_found
            
        # Informational: masses constant
        masses = [b[0] for b in snap0['bodies']]
        for s_idx, snap in enumerate(snapshots[1:]):
            for b_idx in range(3):
                if snap['bodies'][b_idx][0] != masses[b_idx]:
                    detail['errors'].append(f'Mass changed at snapshot {s_idx+1} body {b_idx}')
                    
        # Gate 5: schema
        # We checked bodies and headers. If it gets here cleanly, schema is basically ok.
            
        if detail['errors']:
            detail['status'] = 'fail'
            report['failures'] += 1
        else:
            report['passes'] += 1
            
        report['details'][id_str] = detail
        
    md_path = PROBES_OUT_DIR / "data05_rerun_validation.md"
    json_path = PROBES_OUT_DIR / "data05_rerun_validation.json"
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    with open(md_path, 'w') as f:
        f.write(f"# DATA-05 Rerun Validation Report\n\n")
        f.write(f"Total files: {report['total']}\n")
        f.write(f"Passes: {report['passes']}\n")
        f.write(f"Failures: {report['failures']}\n")
        f.write(f"Missing: {report['missing']}\n\n")
        
        if report['failures'] > 0:
            f.write("## Failures\n")
            for id_str, det in report['details'].items():
                if det['status'] == 'fail':
                    f.write(f"- **{id_str}**\n")
                    for err in det['errors']:
                        f.write(f"  - {err}\n")
                        
    print(f"Validation complete: {report['passes']} passes, {report['failures']} failures.")
    print(f"Report saved to {md_path.relative_to(REPO_ROOT)}")

if __name__ == '__main__':
    main()
