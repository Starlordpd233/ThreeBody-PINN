import os
import sys
import time
import json
import shutil
import pathlib
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor

# IDs: 0005-0059, 0061-0075 (70 total)
IDS = [f"{i:04d}" for i in range(5, 60)] + [f"{i:04d}" for i in range(61, 76)]

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent
BRUTUS_BIN = REPO_ROOT / "brutus_Newton-main" / "brutus"
IC_DIR = REPO_ROOT / "simulation_data" / "Data" / "ic_final" / "ic_hierarchical"
STAGING_DIR = REPO_ROOT / "simulation_data" / "Data" / "rerun_staging" / "data05_gap24-01"

def check_preflight():
    if not BRUTUS_BIN.exists() or not os.access(BRUTUS_BIN, os.X_OK):
        print(f"Error: Brutus binary not found or not executable at {BRUTUS_BIN}")
        sys.exit(1)
    
    missing_ics = []
    for id_str in IDS:
        ic_path = IC_DIR / f"ic_hierarchical_{id_str}.txt"
        if not ic_path.exists():
            missing_ics.append(ic_path)
    
    if missing_ics:
        print(f"Error: Missing {len(missing_ics)} IC files.")
        for p in missing_ics[:5]: print(f"  {p}")
        sys.exit(1)

check_preflight()
STAGING_DIR.mkdir(parents=True, exist_ok=True)

manifest = {}
manifest_lock = threading.Lock()
completed_count = 0
in_flight = {}
in_flight_lock = threading.Lock()
recent_completions = []
start_time_global = time.time()

def clear_screen():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

def dashboard_thread():
    is_tty = sys.stdout.isatty()
    while completed_count < len(IDS):
        if is_tty:
            clear_screen()
            
            elapsed = time.time() - start_time_global
            
            # Estimate ETA
            with manifest_lock:
                durations = [m['duration'] for m in manifest.values() if m['status'] == 'success']
            
            eta_str = "N/A"
            if durations:
                durations.sort()
                median = durations[len(durations)//2]
                remaining = len(IDS) - completed_count
                # roughly divide by workers
                workers_active = max(1, len(in_flight))
                eta_sec = (remaining * median) / workers_active
                eta_str = f"{eta_sec:.1f}s"
            
            pct = (completed_count / len(IDS)) * 100
            
            print(f"=== GAP-24-01 Base-Hierarchical Rerun Dashboard ===")
            print(f"Params: 1e-15 130 0 10 0.08 3")
            print(f"Staging: {STAGING_DIR.relative_to(REPO_ROOT)}")
            print(f"Progress: {completed_count}/{len(IDS)} ({pct:.1f}%) | Elapsed: {elapsed:.1f}s | ETA: {eta_str}")
            print(f"Workers: 14 parallel slots")
            print(f"\n--- In Flight ---")
            with in_flight_lock:
                for wid, (task_id, st) in in_flight.items():
                    print(f"[{wid:02d}] {task_id} ({(time.time() - st):.1f}s)")
            
            print(f"\n--- Recent Completions ---")
            with manifest_lock:
                for rc in recent_completions[-10:]:
                    print(rc)
            
            sys.stdout.flush()
        time.sleep(0.5)

def run_task(task_args):
    global completed_count
    worker_id, id_str = task_args
    
    ic_path = IC_DIR / f"ic_hierarchical_{id_str}.txt"
    out_path = STAGING_DIR / f"brutus_hierarchical_{id_str}.txt"
    
    cmd = [
        str(BRUTUS_BIN),
        '1e-15', '130', '0', '10', '0.08', '3',
        str(ic_path)
    ]
    
    start_t = time.time()
    
    with in_flight_lock:
        in_flight[worker_id] = (id_str, start_t)
        
    status = 'success'
    reason = ''
    try:
        with open(out_path, 'w') as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, timeout=3000, check=True)
        if not out_path.exists() or out_path.stat().st_size == 0:
            status = 'error'
            reason = 'missing or empty output'
    except subprocess.TimeoutExpired:
        status = 'timeout'
        reason = 'timeout 3000s'
    except subprocess.CalledProcessError as e:
        status = 'error'
        reason = f'exit code {e.returncode}'
    
    end_t = time.time()
    dur = end_t - start_t
    
    with manifest_lock:
        manifest[id_str] = {
            'command': cmd,
            'start': start_t,
            'end': end_t,
            'duration': dur,
            'status': status,
            'reason': reason
        }
        mark = "✓" if status == 'success' else "✗"
        res_str = f"{mark} {id_str}: {dur:.1f}s" + (f" [{reason}]" if reason else "")
        recent_completions.append(res_str)
        completed_count += 1
        
    with in_flight_lock:
        if worker_id in in_flight:
            del in_flight[worker_id]
            
    if not sys.stdout.isatty():
        print(f"Completed {id_str} in {dur:.1f}s with status: {status}")

def main():
    print("Starting data05 rerun...")
    
    dash = threading.Thread(target=dashboard_thread, daemon=True)
    dash.start()
    
    tasks = list(enumerate(IDS))
    with ThreadPoolExecutor(max_workers=14) as pool:
        pool.map(run_task, tasks)
        
    # Final save
    manifest_path = STAGING_DIR / "run_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    if sys.stdout.isatty():
        clear_screen()
    print("=== FINAL SUMMARY ===")
    success = sum(1 for m in manifest.values() if m['status'] == 'success')
    print(f"Total Time: {(time.time() - start_time_global):.1f}s")
    print(f"Success: {success}/{len(IDS)}")
    print(f"Manifest written to: {manifest_path.relative_to(REPO_ROOT)}")

if __name__ == '__main__':
    main()
