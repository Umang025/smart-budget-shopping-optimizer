"""
0/1 Knapsack Algorithm Implementation (Dynamic Programming)
For Smart Budget and Shopping Optimizer (DAA Mini Project).

DAA Concept: Dynamic Programming (Bottom-up Tabulation with Backtracking)
Problem Type: Combinatorial Optimization (Whole Items Selection)
Time Complexity: O(n * W) where n = number of products, W = budget capacity
Space Complexity: O(n * W) for full DP table and backtracking
"""

import time
from typing import List, Dict, Any, Tuple


class ZeroOneKnapsack:
    """
    0/1 Knapsack Solver using Dynamic Programming.
    Solves the problem of maximizing total priority/value within a strict budget constraint,
    where items cannot be divided (either taken completely or left out).
    """

    ALGORITHM_NAME = "0/1 Knapsack"
    PARADIGM = "Dynamic Programming"
    TIME_COMPLEXITY = "O(n * W)"
    SPACE_COMPLEXITY = "O(n * W)"

    @staticmethod
    def solve(products: List[Dict[str, Any]], budget: int) -> Dict[str, Any]:
        """
        Executes the 0/1 Knapsack dynamic programming algorithm.

        Args:
            products: List of product dictionaries with 'product_name', 'price', 'priority'.
            budget: Total available shopping budget (integer).

        Returns:
            Dictionary containing:
                - selected_products: List of chosen product dictionaries
                - total_cost: Sum of prices of selected products
                - total_value: Sum of priority values achieved
                - remaining_budget: budget - total_cost
                - execution_time_ms: Run time in milliseconds
                - operations_count: Number of cell calculations in DP table
                - dp_table: 2D table representing optimal values for subproblems
                - explanation: Conceptual explanation for academic viva
        """
        start_time = time.perf_counter()

        n = len(products)
        W = max(0, int(budget))

        # Handle edge cases
        if n == 0 or W == 0:
            return {
                "selected_products": [],
                "total_cost": 0,
                "total_value": 0,
                "remaining_budget": W,
                "execution_time_ms": 0.0,
                "operations_count": 0,
                "dp_table": [[0]],
                "item_names": [],
                "capacity_cols": [0],
                "explanation": "No products available or budget is 0."
            }

        # Step 1: Initialize DP Table of dimensions (n + 1) x (W + 1)
        # dp[i][w] stores maximum value achievable using a subset of first i products with budget w
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        operations_count = 0

        # Step 2: Fill DP Table using Bellman's Principle of Optimality
        for i in range(1, n + 1):
            item = products[i - 1]
            wt = item["price"]
            val = item["priority"]

            for w in range(W + 1):
                operations_count += 1
                if wt <= w:
                    # Item can fit: take max of excluding or including it
                    dp[i][w] = max(dp[i - 1][w], val + dp[i - 1][w - wt])
                else:
                    # Item cannot fit: inherit optimal value from subproblem excluding this item
                    dp[i][w] = dp[i - 1][w]

        max_value = dp[n][W]

        # Step 3: Backtrack to find exact products included in the optimal set
        selected_products = []
        current_w = W
        for i in range(n, 0, -1):
            if dp[i][current_w] != dp[i - 1][current_w]:
                # Product i was included
                item = products[i - 1]
                selected_products.append(item)
                current_w -= item["price"]

        # Backtracked items were collected in reverse order
        selected_products.reverse()

        total_cost = sum(p["price"] for p in selected_products)
        total_value = sum(p["priority"] for p in selected_products)
        remaining_budget = W - total_cost

        elapsed_time = (time.perf_counter() - start_time) * 1000.0

        # Create a simplified sampled DP table for visual representation in GUI
        # If W is large, sample columns to keep table human-readable
        sampled_dp, sampled_cols = ZeroOneKnapsack._sample_dp_table(dp, products, W)

        explanation = (
            f"0/1 Knapsack selected {len(selected_products)} product(s) maximizing priority "
            f"to {total_value} at total cost Rs.{total_cost} within the Rs.{W} budget.\n"
            f"Algorithm evaluated {operations_count:,} subproblems via bottom-up tabulation.\n"
            f"Optimal Substructure Guarantee: Every subproblem solution dp[i][w] is mathematically optimal."
        )

        return {
            "selected_products": selected_products,
            "total_cost": total_cost,
            "total_value": total_value,
            "remaining_budget": remaining_budget,
            "execution_time_ms": round(elapsed_time, 4),
            "operations_count": operations_count,
            "dp_table": dp,
            "sampled_dp": sampled_dp,
            "sampled_cols": sampled_cols,
            "explanation": explanation
        }

    @staticmethod
    def _sample_dp_table(dp: List[List[int]], products: List[Dict[str, Any]], W: int, max_cols: int = 12) -> Tuple[List[List[Any]], List[int]]:
        """
        Creates a readable representation of the DP table for the GUI.
        If budget W has many columns, selects evenly spaced milestones including W.
        """
        n = len(products)
        if W <= max_cols:
            cols = list(range(W + 1))
        else:
            step = max(1, W // (max_cols - 1))
            cols = list(range(0, W, step))
            if cols[-1] != W:
                cols.append(W)

        sampled_rows = []
        for i in range(n + 1):
            row_data = {
                "item_label": "0 (Base)" if i == 0 else f"{products[i-1]['product_name'][:18]} (Rs.{products[i-1]['price']})",
                "values": [dp[i][c] for c in cols]
            }
            sampled_rows.append(row_data)

        return sampled_rows, cols
