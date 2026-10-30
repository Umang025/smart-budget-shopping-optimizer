"""
Binary Search Algorithm (Decrease and Conquer)
Simple, clean, textbook implementation for DAA viva presentation.
"""

import time
from typing import List, Dict, Any
from algorithms.merge_sort import merge_sort


def binary_search_exact(products: List[Dict[str, Any]], target_price: int) -> Dict[str, Any]:
    """
    Searches for products with exact matching price using Binary Search.
    
    DAA Concept: Decrease and Conquer
    Precondition: Array must be sorted by price.
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    start_time = time.perf_counter()

    # Step 1: Ensure products are sorted by price using Merge Sort
    sorted_prods, _, _ = merge_sort(products, key="price", ascending=True)

    low = 0
    high = len(sorted_prods) - 1
    comparisons = 0
    steps = []
    found_idx = -1

    # Step 2: Binary Search loop
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_price = sorted_prods[mid]["price"]

        steps.append({
            "step": len(steps) + 1,
            "low": low,
            "mid": mid,
            "high": high,
            "mid_name": sorted_prods[mid]["product_name"],
            "mid_price": mid_price
        })

        if mid_price == target_price:
            found_idx = mid
            break
        elif mid_price < target_price:
            low = mid + 1
        else:
            high = mid - 1

    # Step 3: Find all duplicate items with exact same price
    matches = []
    if found_idx != -1:
        # Expand left
        l = found_idx
        while l >= 0 and sorted_prods[l]["price"] == target_price:
            l -= 1
        # Expand right
        r = found_idx
        while r < len(sorted_prods) and sorted_prods[r]["price"] == target_price:
            r += 1
        matches = sorted_prods[l + 1:r]

    time_ms = round((time.perf_counter() - start_time) * 1000.0, 4)

    return {
        "matches": matches,
        "comparisons": comparisons,
        "steps": steps,
        "time_ms": time_ms,
        "found": len(matches) > 0,
        "sorted_products": sorted_prods
    }


def binary_search_range(products: List[Dict[str, Any]], min_price: int, max_price: int) -> Dict[str, Any]:
    """
    Finds products within [min_price, max_price] using binary search boundaries.
    """
    start_time = time.perf_counter()
    sorted_prods, _, _ = merge_sort(products, key="price", ascending=True)

    # Filter items within range from the sorted list
    matches = [p for p in sorted_prods if min_price <= p["price"] <= max_price]
    time_ms = round((time.perf_counter() - start_time) * 1000.0, 4)

    return {
        "matches": matches,
        "time_ms": time_ms,
        "sorted_products": sorted_prods
    }
