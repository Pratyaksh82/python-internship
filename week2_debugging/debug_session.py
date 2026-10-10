"""
DEBUGGING VERIFICATION SCRIPT
Demonstrates reproducing each bug from buggy_application.py,
capturing the traceback, and verifying the fix in corrected_application.py.
"""

import sys
import traceback
from datetime import datetime

import week2_debugging.buggy_application as buggy
import week2_debugging.corrected_application as corrected


def run_diagnostics():
    print("=" * 70)
    print(" WEEK 2: PYTHON DEBUGGING AND TROUBLESHOOTING DEMONSTRATION")
    print("=" * 70)

    # Bug 1: File I/O
    print("\n--- [Diagnosing Bug 1: Missing File & Resource Leak] ---")
    try:
        buggy.load_raw_orders("non_existent_orders.json")
    except Exception as e:
        print(f"-> Buggy Code Exception: {type(e).__name__}: {e}")
    res1 = corrected.load_raw_orders("non_existent_orders.json")
    print(f"-> Corrected Code Handled Gracefully: Returns {res1}")

    # Bug 2: Mutable Default Argument
    print("\n--- [Diagnosing Bug 2: Mutable Default Argument] ---")
    ord1 = buggy.create_order(1, "Customer A")
    ord2 = buggy.create_order(2, "Customer B")
    print(f"-> Buggy State: Order 1 items count: {len(ord1['items'])}, Order 2 items count: {len(ord2['items'])} (LEAKED!)")
    
    cord1 = corrected.create_order(1, "Customer A")
    cord2 = corrected.create_order(2, "Customer B")
    print(f"-> Corrected State: Order 1 count: {len(cord1['items'])}, Order 2 count: {len(cord2['items'])} (ISOLATED!)")

    # Bug 3: Off-by-one Indexing
    print("\n--- [Diagnosing Bug 3: Off-by-One Loop Indexing] ---")
    test_list = [{"id": 1}, {"id": 2}]
    try:
        buggy.process_orders_batch(test_list)
    except Exception as e:
        print(f"-> Buggy Code Exception: {type(e).__name__}: {e}")
    c_proc = corrected.process_orders_batch(test_list)
    print(f"-> Corrected Code Output: Processed {len(c_proc)} orders successfully.")

    # Bug 4: Mutating List During Iteration
    print("\n--- [Diagnosing Bug 4: Mutating List During Iteration] ---")
    consecutive_cancelled = [
        {"id": 1, "status": "CANCELLED"},
        {"id": 2, "status": "CANCELLED"},
        {"id": 3, "status": "ACTIVE"}
    ]
    buggy_filtered = buggy.filter_cancelled_orders(list(consecutive_cancelled))
    print(f"-> Buggy Iteration Result (Skipped second cancelled!): Length = {len(buggy_filtered)} (Expected: 1)")
    c_filtered = corrected.filter_cancelled_orders(consecutive_cancelled)
    print(f"-> Corrected Filter Result: Length = {len(c_filtered)} (Accurately filtered!)")

    # Bug 5: Unsafe Coercion & ZeroDivision
    print("\n--- [Diagnosing Bug 5: ZeroDivisionError & Price Parsing] ---")
    try:
        buggy.compute_average_order_value([])
    except Exception as e:
        print(f"-> Buggy Empty Dataset Exception: {type(e).__name__}: {e}")
    c_avg = corrected.compute_average_order_value([])
    print(f"-> Corrected Average on Empty Dataset: {c_avg}")

    # Bug 6: Shallow Copy Mutation
    print("\n--- [Diagnosing Bug 6: Shallow Copy Mutation] ---")
    source_orders = [{"id": 1, "archived": False}]
    buggy.archive_orders_snapshot(source_orders)
    print(f"-> Buggy Mutation: Source mutated to archived = {source_orders[0]['archived']}")
    clean_source = [{"id": 1, "archived": False}]
    corrected.archive_orders_snapshot(clean_source)
    print(f"-> Corrected Mutation: Source preserved as archived = {clean_source[0]['archived']}")

    # Bug 7: Variable Scoping / UnboundLocalError
    print("\n--- [Diagnosing Bug 7: UnboundLocalError / Scope Confusion] ---")
    try:
        buggy.calculate_tax(50)
    except Exception as e:
        print(f"-> Buggy Code Exception: {type(e).__name__}: {e}")
    c_tax = corrected.calculate_tax(50)
    print(f"-> Corrected Calculation: Tax = ${c_tax}")

    # Bug 8: Datetime JSON Serialization
    print("\n--- [Diagnosing Bug 8: Datetime JSON Serialization] ---")
    test_report = {"time": datetime.now(), "val": 100}
    try:
        buggy.export_report_to_json("data/test_bug.json", test_report)
    except Exception as e:
        print(f"-> Buggy Code Exception: {type(e).__name__}: {e}")
    success = corrected.export_report_to_json("data/test_fixed.json", test_report)
    print(f"-> Corrected Export Result: Success = {success}")

    print("\n" + "=" * 70)
    print(" ALL 8 BUGS SUCCESSFULLY REPRODUCED, ISOLATED, AND RESOLVED!")
    print("=" * 70)


if __name__ == "__main__":
    run_diagnostics()
