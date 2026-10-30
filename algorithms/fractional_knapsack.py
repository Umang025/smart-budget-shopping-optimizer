"""
Fractional Knapsack Algorithm Implementation (Greedy Method)
For Smart Budget and Shopping Optimizer (DAA Mini Project).

DAA Concept: Greedy Method (Value-to-Price Ratio Maximization)
Problem Type: Continuous / Fractional Combinatorial Optimization
Time Complexity: O(n log n) due to ratio sorting
Space Complexity: O(n) for sorted items and decision tracking
"""

import time
from typing import List, Dict, Any


class FractionalKnapsack:
    """
    Fractional Knapsack Solver using the Greedy Method.
    Ranks items by priority-to-price ratio (benefit per rupee).
    Items marked as divisible (e.g. daily essentials, dry fruits, coffee)
    can be taken fractionally if the remaining budget is less than the full price.
    Items marked as indivisible (e.g. electronics, accessories) are taken as whole (100%)
    if they fit, or skipped if they exceed the remaining budget.
    """

    ALGORITHM_NAME = "Fractional Knapsack"
    PARADIGM = "Greedy Method"
    TIME_COMPLEXITY = "O(n log n)"
    SPACE_COMPLEXITY = "O(n)"

    @staticmethod
    def _manual_merge_sort_by_ratio(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Manually sorts items in descending order of value-to-price ratio using Merge Sort.
        Does NOT use Python's built-in sort() or sorted().
        """
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = FractionalKnapsack._manual_merge_sort_by_ratio(items[:mid])
        right = FractionalKnapsack._manual_merge_sort_by_ratio(items[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            # Sort descending: higher ratio comes first
            if left[i]["ratio"] >= right[j]["ratio"]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
        while j < len(right):
            merged.append(right[j])
            j += 1

        return merged

    @staticmethod
    def solve(products: List[Dict[str, Any]], budget: float) -> Dict[str, Any]:
        """
        Executes the Greedy Fractional Knapsack algorithm.

        Args:
            products: List of product dictionaries.
            budget: Total shopping budget (can be int or float).

        Returns:
            Dictionary with:
                - selected_products: List of items with fraction, taken_cost, taken_value
                - total_cost: Total money spent
                - total_value: Total value/priority score achieved
                - remaining_budget: Remaining unspent budget
                - sorted_items: All items with calculated ratios in greedy ranking
                - decisions: Step-by-step trace of greedy decisions
                - execution_time_ms: Run time in milliseconds
                - explanation: Academic viva explanation
        """
        start_time = time.perf_counter()
        W = float(budget)

        if not products or W <= 0:
            return {
                "selected_products": [],
                "total_cost": 0.0,
                "total_value": 0.0,
                "remaining_budget": W,
                "sorted_items": [],
                "decisions": [],
                "execution_time_ms": 0.0,
                "explanation": "No products available or budget is zero."
            }

        # Step 1: Compute value-to-price ratio for every product
        ratio_items = []
        for p in products:
            price = float(p.get("price", 1))
            val = float(p.get("priority", 1))
            ratio = val / price if price > 0 else 0.0
            is_div = int(p.get("is_divisible", 0))

            item_copy = dict(p)
            item_copy["ratio"] = ratio
            item_copy["is_divisible"] = is_div
            ratio_items.append(item_copy)

        # Step 2: Sort items in descending order of ratio (Greedy Choice Property)
        ranked_items = FractionalKnapsack._manual_merge_sort_by_ratio(ratio_items)

        # Step 3: Greedy item selection
        remaining = W
        total_cost = 0.0
        total_value = 0.0
        selected_products = []
        decisions = []

        for item in ranked_items:
            if remaining <= 0:
                decisions.append({
                    "product_name": item["product_name"],
                    "ratio": item["ratio"],
                    "action": "Skipped (Budget Exhausted)",
                    "fraction": 0.0,
                    "cost": 0.0,
                    "value": 0.0,
                    "remaining_budget": 0.0
                })
                continue

            price = float(item["price"])
            val = float(item["priority"])
            is_divisible = item["is_divisible"] == 1

            if price <= remaining:
                # Can take 100% of the item
                fraction = 1.0
                cost = price
                gain_val = val
                remaining -= cost
                total_cost += cost
                total_value += gain_val

                sel_item = dict(item)
                sel_item["fraction"] = fraction
                sel_item["taken_cost"] = cost
                sel_item["taken_value"] = gain_val
                selected_products.append(sel_item)

                decisions.append({
                    "product_name": item["product_name"],
                    "ratio": item["ratio"],
                    "action": "Taken Whole (100%)",
                    "fraction": 1.0,
                    "cost": cost,
                    "value": gain_val,
                    "remaining_budget": round(remaining, 2)
                })

            elif is_divisible:
                # Divisible item: take exact fraction to fill the remaining budget
                fraction = remaining / price
                cost = remaining
                gain_val = val * fraction
                remaining = 0.0
                total_cost += cost
                total_value += gain_val

                sel_item = dict(item)
                sel_item["fraction"] = fraction
                sel_item["taken_cost"] = cost
                sel_item["taken_value"] = gain_val
                selected_products.append(sel_item)

                decisions.append({
                    "product_name": item["product_name"],
                    "ratio": item["ratio"],
                    "action": f"Taken Fraction ({round(fraction * 100, 1)}%)",
                    "fraction": fraction,
                    "cost": cost,
                    "value": gain_val,
                    "remaining_budget": 0.0
                })

            else:
                # Indivisible item that exceeds remaining budget: cannot take fractionally
                decisions.append({
                    "product_name": item["product_name"],
                    "ratio": item["ratio"],
                    "action": "Skipped (Indivisible & Exceeds Budget)",
                    "fraction": 0.0,
                    "cost": 0.0,
                    "value": 0.0,
                    "remaining_budget": round(remaining, 2)
                })

        elapsed_time = (time.perf_counter() - start_time) * 1000.0

        explanation = (
            f"Greedy Fractional Knapsack achieved total priority {round(total_value, 2)} "
            f"at cost Rs.{round(total_cost, 2)} with Rs.{round(remaining, 2)} unspent.\n"
            f"Approach: Highest value/price ratio items are selected first.\n"
            f"Divisible items allowed fractional filling of residual budget, ensuring maximum budget efficiency."
        )

        return {
            "selected_products": selected_products,
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2),
            "remaining_budget": round(remaining, 2),
            "sorted_items": ranked_items,
            "decisions": decisions,
            "execution_time_ms": round(elapsed_time, 4),
            "explanation": explanation
        }
