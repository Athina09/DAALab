"""
EXPERIMENT No. 1: Implementation and Performance Analysis of Interpolation Search
"""

import time
import random
import sys


def interpolation_search(arr, target):
    """Find target in sorted array using interpolation search."""
    low = 0
    high = len(arr) - 1

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
    """Find target in sorted array using binary search."""
    low = 0
    high = len(arr) - 1

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
    """Generate a sorted array of uniformly distributed integers."""
    start = random.randint(1, 1000)
    step = random.randint(1, 10)
    return [start + i * step for i in range(size)]


def measure_search_time(search_fn, arr, target, runs=100):
    """Measure average execution time over multiple runs."""
    total_time = 0.0
    for _ in range(runs):
        start = time.perf_counter()
        result = search_fn(arr, target)
        total_time += time.perf_counter() - start
        if result == -1:
            raise ValueError("Target not found during benchmarking")
    return total_time / runs


def run_experiment():
    sizes = [1000, 5000, 10000, 50000, 100000]
    runs = 100

    print("=" * 72)
    print("EXPERIMENT 1: Interpolation Search vs Binary Search")
    print("=" * 72)
    print(f"{'Size':>10} | {'Interpolation (s)':>20} | {'Binary (s)':>15} | {'Speedup':>10}")
    print("-" * 72)

    results = []

    for size in sizes:
        arr = generate_uniform_sorted_array(size)
        target = arr[size // 2]

        interp_time = measure_search_time(interpolation_search, arr, target, runs)
        binary_time = measure_search_time(binary_search, arr, target, runs)
        speedup = binary_time / interp_time if interp_time > 0 else float("inf")

        results.append((size, interp_time, binary_time, speedup))
        print(
            f"{size:>10,} | {interp_time:>20.8f} | {binary_time:>15.8f} | {speedup:>9.2f}x"
        )

    print("-" * 72)
    print("\nAnalysis:")
    print("- Binary Search time complexity: O(log n)")
    print("- Interpolation Search time complexity: O(log log n) for uniformly distributed data")
    print("- On uniformly distributed sorted arrays, interpolation search typically")
    print("  performs fewer comparisons by estimating the probe position directly.")
    print("- Speedup may vary with target position, distribution, and hardware.")


def verify_algorithms():
    """Quick correctness check before benchmarking."""
    arr = generate_uniform_sorted_array(1000)
    for target in [arr[0], arr[500], arr[-1], 999999]:
        interp = interpolation_search(arr, target)
        binary = binary_search(arr, target)
        expected = arr.index(target) if target in arr else -1
        assert interp == expected, f"Interpolation search failed for {target}"
        assert binary == expected, f"Binary search failed for {target}"


if __name__ == "__main__":
    random.seed(42)
    verify_algorithms()
    run_experiment()
