"""
Fractional Knapsack Algorithm (Greedy Method)
Simple, clean, textbook implementation for DAA viva presentation.
"""

import time
from typing import List, Dict, Any


def _merge_sort_by_ratio(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Manual merge sort in descending order of ratio (no built-in sort)."""
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = _merge_sort_by_ratio(items[:mid])
    right = _merge_sort_by_ratio(items[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]["ratio"] >= right[j]["ratio"]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def solve_fractional_knapsack(products: List[Dict[str, Any]], budget: float) -> Dict[str, Any]:
    """
    Solves Fractional Knapsack using the Greedy Method (Value/Price ratio).
    
    DAA Concept: Greedy Method
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    start_time = time.perf_counter()
    W = float(budget)

    if not products or W <= 0:
        return {
            "selected_items": [],
            "total_cost": 0.0,
            "total_value": 0.0,
            "remaining_budget": W,
            "time_ms": 0.0
        }

    # Step 1: Calculate value-to-price ratio for each product
    items_with_ratio = []
    for p in products:
        item = dict(p)
        price = float(item["price"])
        val = float(item["priority"])
        item["ratio"] = val / price if price > 0 else 0.0
        items_with_ratio.append(item)

    # Step 2: Sort items by ratio descending (Greedy choice)
    ranked_items = _merge_sort_by_ratio(items_with_ratio)

    # Step 3: Select items greedily
    remaining = W
    total_cost = 0.0
    total_value = 0.0
    selected_items = []

    for item in ranked_items:
        if remaining <= 0:
            break

        price = float(item["price"])
        val = float(item["priority"])
        is_divisible = item.get("is_divisible", 0) == 1

        if price <= remaining:
            # Take whole item (100%)
            selected_items.append({
                "product_name": item["product_name"],
                "category": item["category"],
                "price": price,
                "priority": val,
                "fraction": 1.0,
                "cost": price,
                "value": val,
                "ratio": item["ratio"]
            })
            total_cost += price
            total_value += val
            remaining -= price
        elif is_divisible:
            # Take fractional portion to fill the remaining budget
            fraction = remaining / price
            cost = remaining
            gain_val = val * fraction

            selected_items.append({
                "product_name": item["product_name"],
                "category": item["category"],
                "price": price,
                "priority": val,
                "fraction": fraction,
                "cost": cost,
                "value": gain_val,
                "ratio": item["ratio"]
            })
            total_cost += cost
            total_value += gain_val
            remaining = 0.0
            break
        else:
            # Indivisible item cannot fit remaining budget -> skip
            continue

    time_ms = round((time.perf_counter() - start_time) * 1000.0, 4)

    return {
        "selected_items": selected_items,
        "total_cost": round(total_cost, 2),
        "total_value": round(total_value, 2),
        "remaining_budget": round(remaining, 2),
        "time_ms": time_ms
    }
