"""
Merge Sort Algorithm Implementation (Divide and Conquer)
For Smart Budget and Shopping Optimizer (DAA Mini Project).

DAA Concept: Divide and Conquer
Paradigm Steps:
  1. Divide: Split the product array into two halves at mid = (low + high) // 2
  2. Conquer: Recursively sort each subarray using Merge Sort
  3. Combine: Merge the two sorted subarrays in linear O(n) time
Time Complexity: Best O(n log n), Average O(n log n), Worst O(n log n)
Space Complexity: O(n) auxiliary space for merge buffers
"""

import time
from typing import List, Dict, Any, Tuple


class MergeSort:
    """
    Manual Merge Sort implementation for sorting shopping products.
    Strictly avoids Python's built-in sort() or sorted().
    Supports arbitrary keys (price, priority, product_name) and directions (ascending/descending).
    """

    ALGORITHM_NAME = "Merge Sort"
    PARADIGM = "Divide and Conquer"
    BEST_TIME = "O(n log n)"
    AVG_TIME = "O(n log n)"
    WORST_TIME = "O(n log n)"
    SPACE_COMPLEXITY = "O(n)"

    def __init__(self):
        self.comparisons = 0
        self.merge_steps = []

    def sort(
        self,
        products: List[Dict[str, Any]],
        key: str = "price",
        ascending: bool = True
    ) -> Tuple[List[Dict[str, Any]], int, float, str]:
        """
        Sorts the products list using manual recursive Merge Sort.

        Args:
            products: List of product dictionaries.
            key: Field to sort by ('price', 'priority', 'product_name', 'product_id').
            ascending: True for ascending order, False for descending order.

        Returns:
            Tuple of (sorted_products_list, comparisons_count, execution_time_ms, explanation)
        """
        self.comparisons = 0
        self.merge_steps = []
        start_time = time.perf_counter()

        # Create a shallow copy of items to avoid mutating caller's original list in place
        items_to_sort = [dict(p) for p in products]

        sorted_items = self._merge_sort_recursive(items_to_sort, key, ascending, depth=0)

        elapsed_time = (time.perf_counter() - start_time) * 1000.0

        direction_str = "Ascending (Low to High)" if ascending else "Descending (High to Low)"
        explanation = (
            f"Merge Sort sorted {len(products)} products by '{key}' in {direction_str} order.\n"
            f"Divide and Conquer: Array was recursively partitioned into subproblems of size 1, "
            f"then merged using {self.comparisons:,} pairwise key comparisons.\n"
            f"Guaranteed Time Complexity: O(n log n) across all input distributions."
        )

        return sorted_items, self.comparisons, round(elapsed_time, 4), explanation

    def _merge_sort_recursive(
        self,
        items: List[Dict[str, Any]],
        key: str,
        ascending: bool,
        depth: int
    ) -> List[Dict[str, Any]]:
        """Internal recursive divide-and-conquer function."""
        # Base case: A list of 0 or 1 item is already sorted
        if len(items) <= 1:
            return items

        # Divide step: calculate midpoint
        mid = len(items) // 2

        # Conquer step: recursively sort left and right halves
        left_half = self._merge_sort_recursive(items[:mid], key, ascending, depth + 1)
        right_half = self._merge_sort_recursive(items[mid:], key, ascending, depth + 1)

        # Combine step: merge the two sorted halves
        return self._merge(left_half, right_half, key, ascending, depth)

    def _merge(
        self,
        left: List[Dict[str, Any]],
        right: List[Dict[str, Any]],
        key: str,
        ascending: bool,
        depth: int
    ) -> List[Dict[str, Any]]:
        """Internal combine/merge routine."""
        merged = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            self.comparisons += 1
            val_left = left[i].get(key, 0)
            val_right = right[j].get(key, 0)

            # Support string comparison for names or numeric comparison for prices/priorities
            if isinstance(val_left, str):
                val_left = val_left.lower()
                val_right = str(val_right).lower()

            if ascending:
                condition = val_left <= val_right
            else:
                condition = val_left >= val_right

            if condition:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        # Append remaining elements from either list
        while i < len(left):
            merged.append(left[i])
            i += 1

        while j < len(right):
            merged.append(right[j])
            j += 1

        if depth < 3:
            self.merge_steps.append({
                "depth": depth,
                "left_count": len(left),
                "right_count": len(right),
                "merged_count": len(merged)
            })

        return merged
