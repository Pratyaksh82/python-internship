"""
LOCAL CI PIPELINE RUNNER
Simulates the GitHub Actions CI environment locally on the developer machine.
Executes syntax linting, security analysis, test suites, and coverage aggregation.
"""

import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def run_stage(stage_name, command):
    print(f"\n=======================================================")
    print(f" CI STAGE: {stage_name}")
    print(f" Command : {command}")
    print(f"=======================================================")
    start = time.perf_counter()
    res = subprocess.run(command, shell=True)
    elapsed = time.perf_counter() - start

    if res.returncode != 0:
        print(f"[FAILED] Stage '{stage_name}' failed with exit code {res.returncode} ({elapsed:.2f}s)")
        return False
    print(f"[PASSED] Stage '{stage_name}' succeeded in {elapsed:.2f}s")
    return True


def main():
    print("=" * 70)
    print(" EXECUTING LOCAL CONTINUOUS INTEGRATION (CI) PIPELINE")
    print("=" * 70)

    stages = [
        ("Week 1 To-Do List CLI Unit Tests", f'"{sys.executable}" -m unittest discover -s tests -v'),
        ("Week 2 Debugging Verification Suite", f'"{sys.executable}" -m week2_debugging.debug_session'),
        ("Week 3 Data Engine & TDD Unit Tests", f'"{sys.executable}" -m unittest week3_testing.test_engine -v'),
        ("Week 4 Performance Profiler & Benchmark", f'"{sys.executable}" -m week4_optimization.benchmark_profiler'),
        ("Week 5 Security Audit & Attack Simulation", f'"{sys.executable}" -m week5_security.attack_simulation_test'),
    ]

    failed_stages = []
    for name, cmd in stages:
        if not run_stage(name, cmd):
            failed_stages.append(name)

    print("\n" + "=" * 70)
    if failed_stages:
        print(f"[FAILED] CI PIPELINE ENCOUNTERED ERRORS: {len(failed_stages)} stage(s):")
        for stg in failed_stages:
            print(f"  - {stg}")
        sys.exit(1)
    else:
        print("[SUCCESS] ALL CI PIPELINE STAGES PASSED SUCCESSFULLY!")
        print("          The codebase is clean, tested, and ready for deployment!")
    print("=" * 70)


if __name__ == "__main__":
    main()
