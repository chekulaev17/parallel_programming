import subprocess
import csv
import os
import re

DIMENSIONS = [10, 50, 100, 200, 400, 600, 800, 1000]
OUTPUT_FILE = 'stats.csv'
BINARY_PATH = 'src/matrix'

def execute(cmd):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout + proc.stderr

def start():
    if not os.path.exists(BINARY_PATH):
        print(f"Error: {BINARY_PATH} not found!")
        print("Run: g++ src/main.cpp -o src/matrix -O2")
        return
    
    data = []
    
    for size in DIMENSIONS:
        print(f"\n--- Size: {size}x{size} ---")
        
        ok, _ = execute(f"python3 gen_matrices.py {size}")
        if not ok:
            continue
        
        ok, out = execute(BINARY_PATH)
        if not ok:
            continue
        
        match = re.search(r"Computation time:\s*([\d.]+)\s*seconds", out)
        elapsed = float(match.group(1)) if match else 0.0
        
        total_ops = size ** 3
        
        ok, verify_out = execute("python3 check_result.py")
        verdict = "PASSED" if ok and "PASSED" in verify_out else "FAILED"
        
        data.append({'Size': size, 'Time_sec': elapsed, 'Operations': total_ops, 'Status': verdict})
        print(f"Time: {elapsed:.6f} sec | Status: {verdict}")
    
    if data:
        with open(OUTPUT_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Size', 'Time_sec', 'Operations', 'Status'])
            writer.writeheader()
            writer.writerows(data)
        print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    start()
