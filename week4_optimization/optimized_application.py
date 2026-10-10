"""
OPTIMIZED APPLICATION: High-Volume Transaction Processing & Analytics Engine
Applies 4 industry-standard Python optimization patterns:
1. Set Membership: Converts blacklist to hash set for O(1) lookups instead of O(M).
2. Efficient String Construction: Replaces `+=` string concatenation with list `.join()`.
3. Memoization / LRU Caching: Caches repeated mathematical computations via `@lru_cache`.
4. Optimized Grouping: Utilizes `collections.defaultdict` for fast single-pass aggregation.
"""

from collections import defaultdict
from functools import lru_cache
import time
from typing import Any, Dict, List, Set


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


@lru_cache(maxsize=128)
def calculate_tier_multiplier_optimized(tier: int) -> float:
    """Optimization 3: Cached with LRU cache, calculated only once per tier."""
    val = 1.0
    for i in range(1, tier * 1000):
        val = (val * 1.0001) % 10.0
    return round(val, 4)


def process_transactions_optimized(transactions: List[Dict[str, Any]], blacklist_accounts: List[str]) -> Dict[str, Any]:
    """
    Executes transaction processing with high-performance algorithms.
    """
    # Optimization 1: Set lookup O(1) average time complexity
    blacklist_set: Set[str] = set(blacklist_accounts)
    filtered_transactions = [
        tx for tx in transactions if tx["account_id"] not in blacklist_set
    ]

    # Optimization 2: Fast list-join string formatting O(N)
    log_chunks = [
        f"TX:{tx['id']}-ACC:{tx['account_id']};" for tx in filtered_transactions[:1000]
    ]
    audit_log = "".join(log_chunks)

    # Optimization 3 & 4: defaultdict and memoized calculations
    account_totals: Dict[str, float] = defaultdict(float)
    for tx in filtered_transactions:
        # Reuses cached float result in ~0.00001ms
        multiplier = calculate_tier_multiplier_optimized(tx["tier"])
        account_totals[tx["account_id"]] += tx["amount"] * multiplier

    return {
        "processed_count": len(filtered_transactions),
        "unique_accounts": len(account_totals),
        "audit_log_length": len(audit_log),
        "total_volume": round(sum(account_totals.values()), 2)
    }


if __name__ == "__main__":
    data = generate_mock_transactions(15000)
    blacklist = [f"ACC_{k}" for k in range(50, 150)]
    
    start = time.perf_counter()
    result = process_transactions_optimized(data, blacklist)
    elapsed = time.perf_counter() - start
    print(f"[Optimized Run] Elapsed Time: {elapsed:.4f}s | Result: {result}")
