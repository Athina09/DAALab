"""
Interpolation Search vs Binary Search — Interactive Chart
Use the controls to change inputs and see the graph update live.
"""

import random
import time
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np


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


def get_target(arr, position):
    n = len(arr)
    if position == "Start":
        return arr[0]
    elif position == "Middle":
        return arr[n // 2]
    elif position == "End":
        return arr[-1]
    else:  # Random
        return arr[random.randint(0, n - 1)]


def measure_time(fn, arr, target, runs):
    total = 0.0
    for _ in range(runs):
        t = time.perf_counter()
        fn(arr, target)
        total += time.perf_counter() - t
    return (total / runs) * 1e6


def run_benchmark(max_size, runs, position):
    sizes = [
        int(max_size * 0.01),
        int(max_size * 0.05),
        int(max_size * 0.1),
        int(max_size * 0.5),
        int(max_size),
    ]
    sizes = [max(s, 10) for s in sizes]

    interp_times, binary_times = [], []
    for size in sizes:
        arr = generate_uniform_sorted_array(size)
        target = get_target(arr, position)
        interp_times.append(measure_time(interpolation_search, arr, target, runs))
        binary_times.append(measure_time(binary_search, arr, target, runs))

    return sizes, interp_times, binary_times


# ── Initial state ────────────────────────────────────────────────────────
random.seed(42)
current_position = "Middle"
init_max_size = 100000
init_runs = 100

sizes, interp_times, binary_times = run_benchmark(init_max_size, init_runs, current_position)
labels = [f"{s:,}" for s in sizes]

# ── Layout ───────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plt.subplots_adjust(left=0.08, right=0.98, bottom=0.32, top=0.92)

fig.suptitle("Interpolation Search vs Binary Search — Interactive", fontsize=13, fontweight="bold")

x = np.arange(len(sizes))
width = 0.35

bars_i = ax1.bar(x - width / 2, interp_times, width, label="Interpolation", color="#4C72B0")
bars_b = ax1.bar(x + width / 2, binary_times, width, label="Binary Search", color="#DD8452")
ax1.set_title("Average Search Time")
ax1.set_xlabel("Array Size (n)")
ax1.set_ylabel("Time (µs)")
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()
ax1.grid(axis="y", linestyle="--", alpha=0.5)

speedups = [b / i if i > 0 else 0 for i, b in zip(interp_times, binary_times)]
(line_speedup,) = ax2.plot(labels, speedups, marker="o", color="#2ca02c", linewidth=2, markersize=7)
ax2.axhline(y=1, color="gray", linestyle="--", linewidth=1)
ax2.set_title("Speedup (Binary / Interpolation)")
ax2.set_xlabel("Array Size (n)")
ax2.set_ylabel("Speedup Factor")
ax2.set_ylim(0, max(speedups) * 1.4 if speedups else 5)
ax2.grid(linestyle="--", alpha=0.5)
speedup_labels = [ax2.text(i, speedups[i], f"{speedups[i]:.2f}x", ha="center", va="bottom", fontsize=8) for i in range(len(speedups))]

status_text = fig.text(0.5, 0.96, "", ha="center", fontsize=9, color="gray")


def redraw(max_size, runs, position):
    global speedup_labels
    status_text.set_text("Running benchmark...")
    fig.canvas.draw()

    sizes, interp_times, binary_times = run_benchmark(int(max_size), int(runs), position)
    labels = [f"{s:,}" for s in sizes]
    speedups = [b / i if i > 0 else 0 for i, b in zip(interp_times, binary_times)]

    # Update bar chart
    for bar, h in zip(bars_i, interp_times):
        bar.set_height(h)
    for bar, h in zip(bars_b, binary_times):
        bar.set_height(h)
    ax1.set_xticklabels(labels)
    ax1.relim()
    ax1.autoscale_view()

    # Update speedup line
    line_speedup.set_ydata(speedups)
    ax2.set_xticklabels(labels)
    ax2.set_ylim(0, max(speedups) * 1.4 if speedups else 5)
    for lbl in speedup_labels:
        lbl.remove()
    speedup_labels = [ax2.text(i, speedups[i], f"{speedups[i]:.2f}x", ha="center", va="bottom", fontsize=8) for i in range(len(speedups))]

    status_text.set_text(f"Target: {position} | Max size: {int(max_size):,} | Runs: {int(runs)}")
    fig.canvas.draw_idle()


# ── Widgets ──────────────────────────────────────────────────────────────
ax_size   = plt.axes([0.10, 0.18, 0.55, 0.03])
ax_runs   = plt.axes([0.10, 0.12, 0.55, 0.03])
ax_radio  = plt.axes([0.72, 0.05, 0.22, 0.18])
ax_button = plt.axes([0.10, 0.05, 0.15, 0.06])

slider_size  = widgets.Slider(ax_size,  "Max Array Size", 1000, 500000, valinit=init_max_size, valstep=1000, color="#4C72B0")
slider_runs  = widgets.Slider(ax_runs,  "Runs per Size",  10,   500,    valinit=init_runs,     valstep=10,   color="#DD8452")
radio        = widgets.RadioButtons(ax_radio, ["Start", "Middle", "End", "Random"], active=1)
btn_update   = widgets.Button(ax_button, "Update Chart", color="#e0f0e0", hovercolor="#b0e0b0")


def on_radio(label):
    global current_position
    current_position = label


def on_update(event):
    redraw(slider_size.val, slider_runs.val, current_position)


radio.on_clicked(on_radio)
btn_update.on_clicked(on_update)

status_text.set_text(f"Target: {current_position} | Max size: {init_max_size:,} | Runs: {init_runs}")
plt.show()
