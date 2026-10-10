"""
BUGGY APPLICATION: E-Commerce Order Processor & Analytics Engine
Simulates a real-world enterprise script containing 8 common, critical Python bugs:
1. Unhandled FileNotFoundError & Resource Leak (missing context manager)
2. Mutable Default Argument in function signature
3. Off-by-One IndexError in sequential processing loop
4. Mutating a list while iterating over it (skipping cancelled orders)
5. Unsafe type coercion and ZeroDivisionError on metrics aggregation
6. Shallow Copy Mutation corrupting historical snapshot records
7. UnboundLocalError / Scope confusion in tax calculation
8. TypeError: Object of type datetime is not JSON serializable
"""

import json
import os
from datetime import datetime


def load_raw_orders(filepath):
    # BUG 1: No with statement (file descriptor leak), crashes on missing file
    f = open(filepath, "r")
    content = f.read()
    data = json.loads(content)
    # File is never closed if exception occurs, or simply forgotten
    return data


def create_order(order_id, customer, items=[]):
    # BUG 2: Mutable default argument! All calls sharing default accumulate items
    items.append({"name": "Processing Fee", "price": "1.50"})
    return {
        "order_id": order_id,
        "customer": customer,
        "items": items,
        "created_at": datetime.now(),
        "status": "PENDING"
    }


def calculate_tax(subtotal, tax_rate=0.08):
    # BUG 7: Variable shadowing & UnboundLocalError if conditional branch triggers
    if subtotal > 100:
        tax = subtotal * tax_rate
    elif subtotal > 0:
        # Typo or missing declaration triggers UnboundLocalError
        tax = tax + (subtotal * 0.05)
    return tax


def process_orders_batch(order_list):
    # BUG 3: Off-by-one indexing error (starts at 1, goes up to len, causing IndexError)
    processed = []
    for i in range(1, len(order_list) + 1):
        order = order_list[i]
        processed.append(order)
    return processed


def filter_cancelled_orders(orders):
    # BUG 4: Modifying list during iteration causes items to be skipped
    for order in orders:
        if order.get("status") == "CANCELLED":
            orders.remove(order)
    return orders


def compute_average_order_value(orders):
    # BUG 5: ZeroDivisionError if orders is empty, plus unsafe float conversion
    total = 0
    for order in orders:
        # Assumes price is clean float, fails if '$' present or None
        for item in order["items"]:
            total += float(item["price"])
    # Crashes if len(orders) == 0
    return total / len(orders)


def archive_orders_snapshot(orders):
    # BUG 6: Shallow copy of list containing mutable dicts mutates original state
    snapshot = list(orders)
    for ord_item in snapshot:
        ord_item["archived"] = True
    return snapshot


def export_report_to_json(filepath, report_data):
    # BUG 8: json.dump fails on datetime objects (TypeError)
    with open(filepath, "w") as f:
        json.dump(report_data, f, indent=4)


if __name__ == "__main__":
    print("[Starting Buggy Application Execution]")
    # Will fail at step 1
    orders = load_raw_orders("data/missing_orders.json")
    print(orders)
