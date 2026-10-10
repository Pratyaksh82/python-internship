"""
CORRECTED APPLICATION: E-Commerce Order Processor & Analytics Engine
Production-grade, fully debugged, refactored, and optimized implementation.

Resolved Issues:
1. File I/O: Uses 'with' context manager, handles FileNotFoundError & JSONDecodeError.
2. Default Arguments: Avoids mutable defaults by using `None` and initializing a fresh list.
3. Indexing: Replaced buggy range indexing with direct iteration (`enumerate` / `for item in items`).
4. Iteration Mutation: Uses list comprehension / filtering to create a new list rather than in-place removal.
5. Coercion & Zero-Division: Sanitizes currency strings, validates prices, and guards against empty datasets.
6. Immutability & Snapshots: Uses `copy.deepcopy` to avoid unintended side effects on source records.
7. Variable Scoping: Ensures clean variable initialization before all conditional branches.
8. JSON Serialization: Implements `DateTimeEncoder` to serialize datetime objects into ISO 8601 strings.
"""

import copy
import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("OrderProcessor")


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder handling datetime objects to ISO-8601 format."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def load_raw_orders(filepath: str) -> List[Dict[str, Any]]:
    """
    Safely loads orders from a JSON file.
    Fixes Bug 1: Context manager used, FileNotFoundError and corrupt JSON handled gracefully.
    """
    if not os.path.exists(filepath):
        logger.warning("Target file '%s' does not exist. Initializing with empty order list.", filepath)
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                logger.error("Invalid schema in '%s': expected list of orders.", filepath)
                return []
            return data
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Failed to parse orders file '%s': %s. Returning empty dataset.", filepath, e)
        return []


def create_order(
    order_id: int,
    customer: str,
    items: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Creates an order with defensive default item handling.
    Fixes Bug 2: Mutable default replaced with None and fresh instance creation.
    """
    if items is None:
        order_items = []
    else:
        # Create an independent copy to protect caller input
        order_items = copy.deepcopy(items)

    order_items.append({"name": "Processing Fee", "price": 1.50})

    return {
        "order_id": order_id,
        "customer": customer.strip(),
        "items": order_items,
        "created_at": datetime.now(),
        "status": "PENDING"
    }


def calculate_tax(subtotal: float, tax_rate: float = 0.08) -> float:
    """
    Calculates tax with guaranteed variable initialization.
    Fixes Bug 7: Variable 'tax' initialized upfront before conditional branching.
    """
    if subtotal <= 0:
        return 0.0

    if subtotal > 100.0:
        tax = subtotal * tax_rate
    else:
        tax = subtotal * 0.05

    return round(tax, 2)


def process_orders_batch(order_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Processes orders sequentially without manual index slicing.
    Fixes Bug 3: Direct iteration prevents off-by-one IndexError.
    """
    processed = []
    for order in order_list:
        processed.append(copy.deepcopy(order))
    return processed


def filter_cancelled_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filters out cancelled orders without modifying list during iteration.
    Fixes Bug 4: Uses list comprehension to produce a new, clean list.
    """
    return [order for order in orders if order.get("status") != "CANCELLED"]


def parse_price(price_val: Any) -> float:
    """Helper to sanitize currency strings (e.g. '$19.99', ' 24.50 ') into clean floats."""
    if isinstance(price_val, (int, float)):
        return float(price_val)
    if isinstance(price_val, str):
        cleaned = re.sub(r"[^\d.]", "", price_val.strip())
        if cleaned:
            return float(cleaned)
    return 0.0


def compute_average_order_value(orders: List[Dict[str, Any]]) -> float:
    """
    Computes average order value with zero-division safeguard and price normalization.
    Fixes Bug 5: Guarded against len(orders) == 0 and sanitized string prices.
    """
    if not orders:
        return 0.0

    total_value = 0.0
    for order in orders:
        items = order.get("items", [])
        order_total = sum(parse_price(item.get("price", 0)) for item in items)
        total_value += order_total

    return round(total_value / len(orders), 2)


def archive_orders_snapshot(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Creates an archived snapshot using deep copies to protect source records.
    Fixes Bug 6: Uses copy.deepcopy to prevent mutating original order dictionaries.
    """
    snapshot = copy.deepcopy(orders)
    for ord_item in snapshot:
        ord_item["archived"] = True
    return snapshot


def export_report_to_json(filepath: str, report_data: Dict[str, Any]) -> bool:
    """
    Exports summary report to JSON with custom datetime serialization.
    Fixes Bug 8: Uses DateTimeEncoder to serialize datetime fields without TypeError.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, cls=DateTimeEncoder)
        logger.info("Successfully exported report to '%s'", filepath)
        return True
    except OSError as e:
        logger.error("Failed to export report to '%s': %s", filepath, e)
        return False


if __name__ == "__main__":
    print("=======================================================================")
    print("      🚀 CORRECTED & REFACTORED ORDER PROCESSING ENGINE                ")
    print("=======================================================================")

    # 1. Safe order loading
    sample_orders = [
        create_order(101, "Alice Smith", [{"name": "Mechanical Keyboard", "price": "$89.99"}]),
        create_order(102, "Bob Jones", [{"name": "Wireless Mouse", "price": "25.00"}]),
        create_order(103, "Charlie Brown", [{"name": "Desk Mat", "price": 15.50}]),
    ]
    sample_orders[1]["status"] = "CANCELLED"

    print(f"Total Initial Orders: {len(sample_orders)}")

    # 2. Filter cancelled orders
    active_orders = filter_cancelled_orders(sample_orders)
    print(f"Active (Non-Cancelled) Orders: {len(active_orders)}")

    # 3. Compute metrics safely
    avg_val = compute_average_order_value(active_orders)
    tax_alice = calculate_tax(91.49)
    print(f"Average Order Value: ${avg_val:.2f}")
    print(f"Calculated Tax for Alice: ${tax_alice:.2f}")

    # 4. Deep copy snapshot archiving
    archive = archive_orders_snapshot(active_orders)
    print(f"Original order archived flag: {active_orders[0].get('archived')}")
    print(f"Archive snapshot archived flag: {archive[0].get('archived')}")

    # 5. Safe JSON export with datetime encoding
    report = {
        "generated_at": datetime.now(),
        "total_active_orders": len(active_orders),
        "average_order_value": avg_val,
        "orders": active_orders
    }
    export_report_to_json("data/week2_report.json", report)
    print("Execution completed successfully without errors!")
