"""
Test script for all 4 DAA Algorithms in Smart Budget Optimizer.
"""

import sys
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from utils.csv_handler import load_products
from algorithms.knapsack import ZeroOneKnapsack
from algorithms.fractional_knapsack import FractionalKnapsack
from algorithms.merge_sort import MergeSort
from algorithms.binary_search import BinarySearch


def main():
    prods = load_products()
    print(f"Total products loaded: {len(prods)}")
    assert len(prods) >= 15, "Expected at least 15 sample products."

    # 1. Test 0/1 Knapsack
    res_01 = ZeroOneKnapsack.solve(prods, budget=5000)
    print("\n--- 0/1 Knapsack (Budget: 5000) ---")
    print(f"Selected: {len(res_01['selected_products'])} items")
    print(f"Total Cost: ₹{res_01['total_cost']}, Total Value: {res_01['total_value']}")
    print(f"Remaining Budget: ₹{res_01['remaining_budget']}")
    print(f"Execution Time: {res_01['execution_time_ms']} ms")
    assert res_01['total_cost'] <= 5000, "Cost exceeded budget!"
    assert res_01['total_value'] > 0, "Value should be positive"

    # 2. Test Fractional Knapsack
    res_frac = FractionalKnapsack.solve(prods, budget=5000)
    print("\n--- Fractional Knapsack (Budget: 5000) ---")
    print(f"Selected: {len(res_frac['selected_products'])} items")
    print(f"Total Cost: ₹{res_frac['total_cost']}, Total Value: {res_frac['total_value']}")
    print(f"Remaining Budget: ₹{res_frac['remaining_budget']}")
    print(f"Execution Time: {res_frac['execution_time_ms']} ms")
    assert res_frac['total_cost'] <= 5000.01, "Cost exceeded budget!"
    # Theoretical property: Fractional Knapsack optimal value >= 0/1 Knapsack optimal value
    assert res_frac['total_value'] >= res_01['total_value'], "Fractional knapsack should achieve >= 0/1 value"

    # 3. Test Merge Sort
    sorter = MergeSort()
    sorted_asc, comps_asc, t_asc, _ = sorter.sort(prods, key="price", ascending=True)
    print("\n--- Merge Sort (Price Ascending) ---")
    print(f"Items: {len(sorted_asc)}, Comparisons: {comps_asc}, Time: {t_asc} ms")
    print(f"Min price: ₹{sorted_asc[0]['price']}, Max price: ₹{sorted_asc[-1]['price']}")
    for i in range(len(sorted_asc) - 1):
        assert sorted_asc[i]['price'] <= sorted_asc[i+1]['price'], "List not sorted ascending!"

    sorted_desc, comps_desc, t_desc, _ = sorter.sort(prods, key="priority", ascending=False)
    print("\n--- Merge Sort (Priority Descending) ---")
    print(f"Max priority: {sorted_desc[0]['priority']}, Min priority: {sorted_desc[-1]['priority']}")
    for i in range(len(sorted_desc) - 1):
        assert sorted_desc[i]['priority'] >= sorted_desc[i+1]['priority'], "List not sorted descending!"

    # 4. Test Binary Search
    target_price = sorted_asc[4]['price']
    res_bs = BinarySearch.search_by_exact_price(prods, target_price)
    print(f"\n--- Binary Search (Target: ₹{target_price}) ---")
    print(f"Found: {res_bs['found']}, Matching: {len(res_bs['matching_products'])} items, Steps: {len(res_bs['steps'])}")
    assert res_bs['found'], f"Should have found item with price {target_price}"

    res_range = BinarySearch.search_by_price_range(prods, 500, 1500)
    print("\n--- Binary Search Range (₹500 to ₹1500) ---")
    print(f"Items in range: {len(res_range['matching_products'])}")
    for item in res_range['matching_products']:
        assert 500 <= item['price'] <= 1500, f"Item price {item['price']} outside range!"

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    main()
