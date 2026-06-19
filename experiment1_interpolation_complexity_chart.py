"""
Interpolation Search — Simple Time Complexity Chart
"""

import random
import time
import math
import matplotlib.pyplot as plt


def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high and target >= arr[low] and target <= arr[high]:
        if low == high:
            return low if arr[low] == target else -1
        if arr[high] == arr[low]:
            return low if arr[low] == target else -1
        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1


def generate_uniform_sorted_array(size):
    start = random.randint(1, 1000)
    step = random.randint(1, 10)
    return [start + i * step for i in range(size)]


def measure_time(arr, target, runs=100):
    total = 0.0
    for _ in range(runs):
        t = time.perf_counter()
        interpolation_search(arr, target)
        total += time.perf_counter() - t
    return (total / runs) * 1e6  # microseconds


random.seed(42)

sizes = [1000, 5000, 10000, 50000, 100000]
times = []

for size in sizes:
    arr = generate_uniform_sorted_array(size)
    target = arr[size // 2]
    times.append(measure_time(arr, target))

labels = [f"{s:,}" for s in sizes]

# Theoretical O(log log n) — scaled to match measured range
theory = [math.log2(math.log2(n)) for n in sizes]
scale = times[-1] / theory[-1]
theory_scaled = [v * scale for v in theory]

# Plot
plt.figure(figsize=(8, 5))
plt.plot(labels, times, marker="o", color="#4C72B0", linewidth=2, markersize=7, label="Measured Time")
plt.plot(labels, theory_scaled, marker="^", linestyle="--", color="#2ca02c", linewidth=1.5, markersize=6, label="O(log log n) — theoretical")

for i, (lbl, t) in enumerate(zip(labels, times)):
    plt.annotate(f"{t:.3f} µs", (lbl, t), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)

plt.title("Interpolation Search — Time Complexity", fontsize=13, fontweight="bold")
plt.xlabel("Array Size (n)")
plt.ylabel("Time (microseconds)")
plt.legend()
plt.grid(linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("experiment1_interpolation_complexity_chart.png", dpi=150)
print("Chart saved to experiment1_interpolation_complexity_chart.png")
plt.show()
