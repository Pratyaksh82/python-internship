"""
BASELINE APPLICATION: High-Volume Transaction Processing & Analytics Engine
Contains 4 common real-world algorithmic and resource bottlenecks:
1. O(N^2) search: List membership lookup inside loops instead of O(1) set.
2. Inefficient string concatenation: Using `+=` inside loops.
3. Redundant repeated computation: Uncached mathematical fee calculations.
4. Nested linear scans: Manual quadratic grouping instead of hash map.
"""

import time
from typing import Any, Dict, List


def generate_mock_transactions(count: int = 15000) -> List[Dict[str, Any]]:
    """Generates synthetic transaction records for benchmarking."""
    records = []
    for i in range(count):
        records.append({
            "id": i,
            "account_id": f"ACC_{i % 500}",
            "amount": float((i * 17) % 500 + 10),
            "tier": (i % 5) + 1,
            "status": "APPROVED" if i % 7 != 0 else "FLAGGED"
        })
    return records


def calculate_tier_multiplier_unmemoized(tier: int) -> float:
    """Bottleneck 3: Simulates repeated non-cached computation."""
    val = 1.0
    for i in range(1, tier * 1000):
        val = (val * 1.0001) % 10.0
    return round(val, 4)


def process_transactions_baseline(transactions: List[Dict[str, Any]], blacklist_accounts: List[str]) -> Dict[str, Any]:
    """
    Executes transaction processing with intentional bottlenecks.
    """
    # Bottleneck 1: blacklist_accounts is a LIST -> O(N * M) lookup
    filtered_transactions = []
    for tx in transactions:
        if tx["account_id"] not in blacklist_accounts:  # O(M) search
            filtered_transactions.append(tx)

    # Bottleneck 2: Repeated string concatenation via +=
    audit_log = ""
    for tx in filtered_transactions[:1000]:
        audit_log += f"TX:{tx['id']}-ACC:{tx['account_id']};"  # Quadratic string reallocation

    # Bottleneck 3 & 4: Nested grouping & redundant unmemoized multiplier calculation
    account_totals = {}
    for tx in filtered_transactions:
        acc = tx["account_id"]
        # Multiplier recomputed 15,000 times for only 5 possible tiers
        multiplier = calculate_tier_multiplier_unmemoized(tx["tier"])
        adj_amount = tx["amount"] * multiplier
        
        # Quadratic linear lookup check
        if acc not in account_totals:
            account_totals[acc] = 0.0
        account_totals[acc] += adj_amount

    return {
        "processed_count": len(filtered_transactions),
        "unique_accounts": len(account_totals),
        "audit_log_length": len(audit_log),
        "total_volume": round(sum(account_totals.values()), 2)
    }


if __name__ == "__main__":
    data = generate_mock_transactions(15000)
    blacklist = [f"ACC_{k}" for k in range(50, 150)]  # 100 blacklist items
    
    start = time.perf_counter()
    result = process_transactions_baseline(data, blacklist)
    elapsed = time.perf_counter() - start
    print(f"[Baseline Run] Elapsed Time: {elapsed:.4f}s | Result: {result}")
