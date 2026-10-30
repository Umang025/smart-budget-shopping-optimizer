"""
Binary Search Algorithm Implementation (Decrease and Conquer)
For Smart Budget and Shopping Optimizer (DAA Mini Project).

DAA Concept: Decrease and Conquer / Divide and Conquer
Precondition: Input array MUST be sorted by the search key (Price)
Time Complexity: Best O(1), Average O(log n), Worst O(log n)
Space Complexity: O(1) iterative
"""

import time
from typing import List, Dict, Any, Tuple
from algorithms.merge_sort import MergeSort


class BinarySearch:
    """
    Manual Binary Search implementation for product catalog querying.
    Strictly avoids Python's bisect module.
    Includes:
      1. Exact price search (handles duplicates by gathering adjacent identical price items)
      2. Price range search (finds lower and upper bounds using binary search)
    """

    ALGORITHM_NAME = "Binary Search"
    PARADIGM = "Decrease and Conquer"
    BEST_TIME = "O(1)"
    AVG_TIME = "O(log n)"
    WORST_TIME = "O(log n)"
    SPACE_COMPLEXITY = "O(1)"

    @staticmethod
    def search_by_exact_price(
        products: List[Dict[str, Any]],
        target_price: int
    ) -> Dict[str, Any]:
        """
        Searches for products with an exact matching price.
        First ensures products are sorted using manual Merge Sort.
        Then performs manual binary search with step logging.

        Args:
            products: List of product dictionaries.
            target_price: Target price to search for.

        Returns:
            Dictionary containing:
                - matching_products: All items matching target_price
                - steps: Tracing list of (low, mid, high, mid_price, action)
                - comparisons: Total comparisons made
                - execution_time_ms: Search execution time
                - sorted_products: List of products sorted by price
                - explanation: Academic explanation
        """
        start_time = time.perf_counter()

        # Step 1: Precondition - Guarantee list is sorted by price using Merge Sort
        sorter = MergeSort()
        sorted_products, sort_comparisons, _, _ = sorter.sort(products, key="price", ascending=True)

        n = len(sorted_products)
        low = 0
        high = n - 1
        steps = []
        comparisons = 0
        found_index = -1

        # Step 2: Binary Search Loop
        while low <= high:
            comparisons += 1
            mid = (low + high) // 2
            mid_price = sorted_products[mid]["price"]

            step_info = {
                "step_num": len(steps) + 1,
                "low": low,
                "high": high,
                "mid": mid,
                "mid_product": sorted_products[mid]["product_name"],
                "mid_price": mid_price,
                "target_price": target_price,
            }

            if mid_price == target_price:
                step_info["action"] = f"Match Found at index {mid} (Rs.{mid_price} == Rs.{target_price})"
                steps.append(step_info)
                found_index = mid
                break
            elif mid_price < target_price:
                step_info["action"] = f"Rs.{mid_price} < Rs.{target_price} -> Search Right half (low = {mid + 1})"
                steps.append(step_info)
                low = mid + 1
            else:
                step_info["action"] = f"Rs.{mid_price} > Rs.{target_price} -> Search Left half (high = {mid - 1})"
                steps.append(step_info)
                high = mid - 1

        # Step 3: Handle duplicate prices around found_index (if any)
        matching_products = []
        if found_index != -1:
            # Expand left
            l = found_index
            while l >= 0 and sorted_products[l]["price"] == target_price:
                l -= 1

            # Expand right
            r = found_index
            while r < n and sorted_products[r]["price"] == target_price:
                r += 1

            matching_products = sorted_products[l + 1:r]

        elapsed_time = (time.perf_counter() - start_time) * 1000.0

        if matching_products:
            explanation = (
                f"Binary Search located {len(matching_products)} product(s) priced at Rs.{target_price} in "
                f"{len(steps)} probe step(s) with {comparisons} comparisons.\n"
                f"Halving Principle: Search space reduced by half at each step (O(log n) search time)."
            )
        else:
            explanation = (
                f"Target price Rs.{target_price} not found in catalog after {len(steps)} probe step(s).\n"
                f"Interval converged (low > high), confirming no matching product exists."
            )

        return {
            "matching_products": matching_products,
            "steps": steps,
            "comparisons": comparisons,
            "execution_time_ms": round(elapsed_time, 4),
            "sorted_products": sorted_products,
            "found": len(matching_products) > 0,
            "explanation": explanation
        }

    @staticmethod
    def search_by_price_range(
        products: List[Dict[str, Any]],
        min_price: int,
        max_price: int
    ) -> Dict[str, Any]:
        """
        Finds all products whose price falls within [min_price, max_price]
        using Binary Search boundary queries (Lower Bound and Upper Bound).
        """
        start_time = time.perf_counter()

        sorter = MergeSort()
        sorted_products, _, _, _ = sorter.sort(products, key="price", ascending=True)

        n = len(sorted_products)
        if n == 0 or min_price > max_price:
            return {
                "matching_products": [],
                "lower_bound_idx": -1,
                "upper_bound_idx": -1,
                "comparisons": 0,
                "execution_time_ms": 0.0,
                "sorted_products": sorted_products,
                "explanation": "Empty list or invalid price range (min > max)."
            }

        # 1. Binary Search for Lower Bound: First index where price >= min_price
        low, high = 0, n - 1
        lower_bound = n
        comparisons = 0
        while low <= high:
            comparisons += 1
            mid = (low + high) // 2
            if sorted_products[mid]["price"] >= min_price:
                lower_bound = mid
                high = mid - 1
            else:
                low = mid + 1

        # 2. Binary Search for Upper Bound: Last index where price <= max_price
        low, high = 0, n - 1
        upper_bound = -1
        while low <= high:
            comparisons += 1
            mid = (low + high) // 2
            if sorted_products[mid]["price"] <= max_price:
                upper_bound = mid
                low = mid + 1
            else:
                high = mid - 1

        matching_products = []
        if lower_bound <= upper_bound and lower_bound < n and upper_bound >= 0:
            matching_products = sorted_products[lower_bound:upper_bound + 1]

        elapsed_time = (time.perf_counter() - start_time) * 1000.0

        explanation = (
            f"Range Binary Search found {len(matching_products)} product(s) in range [Rs.{min_price}, Rs.{max_price}].\n"
            f"Determined lower bound at index {lower_bound} and upper bound at index {upper_bound} "
            f"using two logarithmic binary search passes ({comparisons} comparisons total)."
        )

        return {
            "matching_products": matching_products,
            "lower_bound_idx": lower_bound,
            "upper_bound_idx": upper_bound,
            "comparisons": comparisons,
            "execution_time_ms": round(elapsed_time, 4),
            "sorted_products": sorted_products,
            "explanation": explanation
        }
