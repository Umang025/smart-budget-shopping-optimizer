"""
0/1 Knapsack Algorithm (Dynamic Programming)
Simple, clean, textbook implementation for DAA viva presentation.
"""

import time
from typing import List, Dict, Any


def solve_01_knapsack(products: List[Dict[str, Any]], budget: int) -> Dict[str, Any]:
    """
    Solves 0/1 Knapsack using Dynamic Programming (Bottom-Up Tabulation).
    
    DAA Concept: Dynamic Programming
    Time Complexity: O(n * W)
    Space Complexity: O(n * W)
    """
    start_time = time.perf_counter()

    n = len(products)
    W = max(0, int(budget))

    if n == 0 or W == 0:
        return {
            "selected_items": [],
            "total_cost": 0,
            "total_value": 0,
            "remaining_budget": W,
            "time_ms": 0.0,
            "dp_table": [[0]]
        }

    # Step 1: Create DP Table of size (n + 1) x (W + 1)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Step 2: Fill DP Table using Bellman's principle of optimality
    for i in range(1, n + 1):
        item = products[i - 1]
        price = item["price"]
        val = item["priority"]

        for w in range(W + 1):
            if price <= w:
                # Max of excluding item OR including item
                dp[i][w] = max(dp[i - 1][w], val + dp[i - 1][w - price])
            else:
                # Cannot include item, carry over previous value
                dp[i][w] = dp[i - 1][w]

    # Step 3: Backtrack to find which items were selected
    selected_items = []
    current_w = W
    for i in range(n, 0, -1):
        if dp[i][current_w] != dp[i - 1][current_w]:
            item = products[i - 1]
            selected_items.append(item)
            current_w -= item["price"]

    selected_items.reverse()
    total_cost = sum(p["price"] for p in selected_items)
    total_value = dp[n][W]
    time_ms = round((time.perf_counter() - start_time) * 1000.0, 4)

    return {
        "selected_items": selected_items,
        "total_cost": total_cost,
        "total_value": total_value,
        "remaining_budget": W - total_cost,
        "time_ms": time_ms,
        "dp_table": dp
    }
