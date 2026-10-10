"""
PROFILING AND BENCHMARKING HARNESS (Week 4)
Leverages cProfile, pstats, and time.perf_counter to evaluate baseline vs optimized code.
Validates functional equivalence and prints benchmark comparison metrics.
"""

import cProfile
import pstats
import io
import time
from week4_optimization.baseline_application import (
    generate_mock_transactions,
    process_transactions_baseline
)
from week4_optimization.optimized_application import (
    process_transactions_optimized
)


def run_benchmarks():
    print("=" * 70)
    print(" WEEK 4: PYTHON PERFORMANCE OPTIMIZATION & PROFILING BENCHMARK")
    print("=" * 70)

    dataset_size = 20000
    print(f"\n[1] Generating Synthetic Dataset: {dataset_size} transactions...")
    transactions = generate_mock_transactions(dataset_size)
    blacklist = [f"ACC_{i}" for i in range(50, 150)]  # 100 blacklist accounts

    # --- Profile Baseline ---
    print("\n[2] Profiling Baseline Implementation...")
    pr_baseline = cProfile.Profile()
    pr_baseline.enable()
    start_b = time.perf_counter()
    baseline_result = process_transactions_baseline(transactions, blacklist)
    elapsed_baseline = time.perf_counter() - start_b
    pr_baseline.disable()

    # --- Profile Optimized ---
    print("\n[3] Profiling Optimized Implementation...")
    pr_optimized = cProfile.Profile()
    pr_optimized.enable()
    start_o = time.perf_counter()
    optimized_result = process_transactions_optimized(transactions, blacklist)
    elapsed_optimized = time.perf_counter() - start_o
    pr_optimized.disable()

    # --- Functional Equivalence Check ---
    print("\n[4] Validating Functional Equivalence...")
    assert baseline_result == optimized_result, f"Discrepancy detected: {baseline_result} != {optimized_result}"
    print("-> Functional Equivalence Confirmed: Both implementations produce identical results!")

    # --- Print Comparison ---
    speedup = elapsed_baseline / elapsed_optimized if elapsed_optimized > 0 else 0.0
    print("\n" + "=" * 70)
    print(" PERFORMANCE BENCHMARK COMPARISON SUMMARY")
    print("=" * 70)
    print(f" Dataset Size        : {dataset_size} records")
    print(f" Baseline Runtime    : {elapsed_baseline:.4f} seconds")
    print(f" Optimized Runtime   : {elapsed_optimized:.4f} seconds")
    print(f" Execution Speedup   : {speedup:.2f}x FASTER")
    print(f" Latency Reduction   : {((elapsed_baseline - elapsed_optimized) / elapsed_baseline) * 100:.2f}%")
    print("=" * 70)

    # Output top function calls for baseline
    s_b = io.StringIO()
    ps_b = pstats.Stats(pr_baseline, stream=s_b).sort_stats("cumulative")
    ps_b.print_stats(5)
    print("\n[Top 5 Baseline Profile Calls]:\n", s_b.getvalue())

    # Output top function calls for optimized
    s_o = io.StringIO()
    ps_o = pstats.Stats(pr_optimized, stream=s_o).sort_stats("cumulative")
    ps_o.print_stats(5)
    print("[Top 5 Optimized Profile Calls]:\n", s_o.getvalue())


if __name__ == "__main__":
    run_benchmarks()
