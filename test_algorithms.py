"""
Test script for all 4 DAA Algorithms in Smart Budget Optimizer.
"""

import sys
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from utils.csv_handler import load_products
from algorithms.knapsack import solve_01_knapsack
from algorithms.fractional_knapsack import solve_fractional_knapsack
from algorithms.merge_sort import merge_sort
from algorithms.binary_search import binary_search_exact, binary_search_range


def main():
    prods = load_products()
    print(f"Total products loaded: {len(prods)}")
    assert len(prods) >= 15, "Expected at least 15 sample products."

    # 1. Test 0/1 Knapsack
    res_01 = solve_01_knapsack(prods, budget=5000)
    print("\n--- 1. 0/1 Knapsack (Dynamic Programming) ---")
    print(f"Selected: {len(res_01['selected_items'])} items")
    print(f"Total Cost: Rs.{res_01['total_cost']}, Total Value: {res_01['total_value']}")
    print(f"Remaining Budget: Rs.{res_01['remaining_budget']}, Time: {res_01['time_ms']} ms")
    assert res_01['total_cost'] <= 5000

    # 2. Test Fractional Knapsack
    res_frac = solve_fractional_knapsack(prods, budget=5000)
    print("\n--- 2. Fractional Knapsack (Greedy Method) ---")
    print(f"Selected: {len(res_frac['selected_items'])} items")
    print(f"Total Cost: Rs.{res_frac['total_cost']}, Total Value: {res_frac['total_value']}")
    print(f"Remaining Budget: Rs.{res_frac['remaining_budget']}, Time: {res_frac['time_ms']} ms")
    assert res_frac['total_cost'] <= 5000.01
    assert res_frac['total_value'] >= res_01['total_value']

    # 3. Test Merge Sort
    sorted_asc, comps_asc, t_asc = merge_sort(prods, key="price", ascending=True)
    print("\n--- 3. Merge Sort (Divide and Conquer) ---")
    print(f"Items: {len(sorted_asc)}, Comparisons: {comps_asc}, Time: {t_asc} ms")
    print(f"Min price: Rs.{sorted_asc[0]['price']}, Max price: Rs.{sorted_asc[-1]['price']}")
    for i in range(len(sorted_asc) - 1):
        assert sorted_asc[i]['price'] <= sorted_asc[i+1]['price']

    # 4. Test Binary Search
    target = sorted_asc[5]['price']
    res_bs = binary_search_exact(prods, target)
    print(f"\n--- 4. Binary Search (Exact Price: Rs.{target}) ---")
    print(f"Found: {res_bs['found']}, Matches: {len(res_bs['matches'])}, Comparisons: {res_bs['comparisons']}")
    assert res_bs['found']

    res_range = binary_search_range(prods, 500, 1500)
    print(f"Range Search (Rs.500 to Rs.1500): {len(res_range['matches'])} matches found")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    main()
