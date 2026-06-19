"""
Chart generator for Experiment 1: Interpolation Search vs Binary Search
"""

import random
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


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


def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def generate_uniform_sorted_array(size):
    start = random.randint(1, 1000)
    step = random.randint(1, 10)
    return [start + i * step for i in range(size)]


def measure_search_time(search_fn, arr, target, runs=100):
    total = 0.0
    for _ in range(runs):
        t = time.perf_counter()
        search_fn(arr, target)
        total += time.perf_counter() - t
    return total / runs


def collect_data():
    sizes = [1000, 5000, 10000, 50000, 100000]
    interp_times, binary_times, speedups = [], [], []

    for size in sizes:
        arr = generate_uniform_sorted_array(size)
        target = arr[size // 2]
        it = measure_search_time(interpolation_search, arr, target)
        bt = measure_search_time(binary_search, arr, target)
        interp_times.append(it * 1e6)   # convert to microseconds
        binary_times.append(bt * 1e6)
        speedups.append(bt / it if it > 0 else 0)

    return sizes, interp_times, binary_times, speedups


def plot(sizes, interp_times, binary_times, speedups):
    labels = [f"{s:,}" for s in sizes]
    x = range(len(sizes))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Experiment 1: Interpolation Search vs Binary Search", fontsize=14, fontweight="bold")

    # --- Chart 1: Time comparison (grouped bar) ---
    ax1 = axes[0]
    width = 0.35
    bars1 = ax1.bar([i - width / 2 for i in x], interp_times, width, label="Interpolation Search", color="#4C72B0")
    bars2 = ax1.bar([i + width / 2 for i in x], binary_times, width, label="Binary Search", color="#DD8452")

    ax1.set_title("Average Search Time per Array Size")
    ax1.set_xlabel("Array Size (n)")
    ax1.set_ylabel("Time (microseconds)")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(labels)
    ax1.legend()
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.3f µs"))
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                 f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=7.5, color="#4C72B0")
    for bar in bars2:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                 f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=7.5, color="#DD8452")

    # --- Chart 2: Speedup line ---
    ax2 = axes[1]
    ax2.plot(labels, speedups, marker="o", color="#2ca02c", linewidth=2, markersize=7, label="Speedup (Binary / Interpolation)")
    ax2.axhline(y=1, color="gray", linestyle="--", linewidth=1, label="Baseline (1x)")
    for i, (lbl, s) in enumerate(zip(labels, speedups)):
        ax2.annotate(f"{s:.2f}x", (lbl, s), textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=9, color="#2ca02c")

    ax2.set_title("Speedup of Interpolation Search over Binary Search")
    ax2.set_xlabel("Array Size (n)")
    ax2.set_ylabel("Speedup Factor")
    ax2.set_ylim(0, max(speedups) * 1.3)
    ax2.legend()
    ax2.grid(linestyle="--", alpha=0.5)

    plt.tight_layout()
    out = "experiment1_chart.png"
    plt.savefig(out, dpi=150)
    print(f"Chart saved to {out}")
    plt.show()


if __name__ == "__main__":
    random.seed(42)
    sizes, interp_times, binary_times, speedups = collect_data()
    plot(sizes, interp_times, binary_times, speedups)
