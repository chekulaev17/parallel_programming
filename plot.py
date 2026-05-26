import matplotlib.pyplot as plt
import csv

dims = []
elapsed = []

with open('stats.csv', 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
        dims.append(int(line['Size']))
        elapsed.append(float(line['Time_sec']))

plt.figure(figsize=(10, 6))
plt.plot(dims, elapsed, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (seconds)')
plt.title('Matrix multiplication time')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('graph_time.png')
print("graph_time.png saved")

plt.figure(figsize=(10, 6))
plt.plot(dims, [d**3 for d in dims], 'ro-', linewidth=2, markersize=8)
plt.xlabel('Matrix size (N)')
plt.ylabel('Operations')
plt.title('Operations vs matrix size')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('graph_ops.png')
print("graph_ops.png saved")
