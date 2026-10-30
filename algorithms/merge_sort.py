"""
Merge Sort Algorithm (Divide and Conquer)
Simple, clean, textbook implementation for DAA viva presentation.
"""

import time
from typing import List, Dict, Any, Tuple


def merge_sort(
    items: List[Dict[str, Any]],
    key: str = "price",
    ascending: bool = True
) -> Tuple[List[Dict[str, Any]], int, float]:
    """
    Sorts product dictionaries using recursive Merge Sort.
    
    DAA Concept: Divide and Conquer
    Time Complexity: O(n log n) in all cases (Best, Average, Worst)
    Space Complexity: O(n)
    
    Returns:
        (sorted_list, comparison_count, time_in_ms)
    """
    comparisons = [0]  # mutable counter
    start_time = time.perf_counter()

    def _sort(sub_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Base case
        if len(sub_list) <= 1:
            return sub_list

        # Divide step
        mid = len(sub_list) // 2
        left = _sort(sub_list[:mid])
        right = _sort(sub_list[mid:])

        # Combine step (merge)
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            val_l = left[i].get(key, 0)
            val_r = right[j].get(key, 0)

            # Handle string case insensitivity
            if isinstance(val_l, str):
                val_l = val_l.lower()
                val_r = str(val_r).lower()

            if (val_l <= val_r) if ascending else (val_l >= val_r):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_result = _sort(list(items))
    time_ms = round((time.perf_counter() - start_time) * 1000.0, 4)

    return sorted_result, comparisons[0], time_ms
