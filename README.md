# Smart Budget and Shopping Optimizer

**MCA (Cloud Computing and DevOps) — Design and Analysis of Algorithms (DAA) Mini Project**

A streamlined, beginner-friendly desktop application that solves shopping budget optimization using **four standard DAA algorithms** implemented from scratch in pure Python with a modern dark GUI.

---

## 1. The Four DAA Algorithms (Simplified)

| # | Algorithm | DAA Paradigm | Time Complexity | Space | Why We Use It |
|---|---|---|:---:|:---:|---|
| **1** | **0/1 Knapsack** | **Dynamic Programming** | $O(n \cdot W)$ | $O(n \cdot W)$ | Finds the best combination of whole items within a fixed budget by solving subproblems using a 2D table (`dp[i][w]`). |
| **2** | **Fractional Knapsack** | **Greedy Method** | $O(n \log n)$ | $O(n)$ | Sorts items by value-to-price ratio (`priority / price`) and greedily picks items. Allows partial quantities for divisible goods (e.g. coffee, dry fruits). |
| **3** | **Merge Sort** | **Divide and Conquer** | $O(n \log n)$ | $O(n)$ | Recursively splits product list in half and merges them back in sorted order (by price or priority) without using Python's built-in sort. |
| **4** | **Binary Search** | **Decrease and Conquer** | $O(\log n)$ | $O(1)$ | Repeatedly halves the search space to find products at a specific price in logarithmic time. |

---

## 2. Project Files

```text
smart-budget-shopping-optimizer/
│
├── main.py                     # Clean app window & navigation sidebar
├── products.csv                # CSV database of products
├── requirements.txt            # Dependencies (customtkinter, matplotlib, pillow)
├── test_algorithms.py          # Quick test script for all 4 algorithms
├── run_app.bat                 # One-click Windows launcher
│
├── algorithms/                 # Clean, textbook DAA algorithm files (~40-60 lines each)
│   ├── knapsack.py             # 0/1 Knapsack (DP tabulation + backtracking)
│   ├── fractional_knapsack.py  # Fractional Knapsack (Greedy ratio selection)
│   ├── merge_sort.py           # Merge Sort (Divide & Conquer)
│   └── binary_search.py        # Binary Search (Exact & range query)
│
├── gui/                        # Simple, clean user interface pages
│   ├── dashboard.py            # Overview statistics + category bar chart
│   ├── product_manager.py      # Add, view, filter, and delete products (updates CSV)
│   ├── optimizer.py            # Side-by-side 0/1 Knapsack (DP) vs Fractional (Greedy)
│   ├── search_sort.py          # Sort products & Binary Search by price
│   └── algorithm_analysis.py   # Complexity table + live benchmark runtime curve
│
└── utils/
    └── csv_handler.py          # Direct CSV read/write and validation
```

---

## 3. How to Run

### Step 1: Install requirements
```bash
pip install -r requirements.txt
```

### Step 2: Test the algorithms
```bash
python test_algorithms.py
```

### Step 3: Launch the application
```bash
python main.py
```
*(Or double-click `run_app.bat` on Windows)*

---

## 4. Key Viva Questions & Answers

1. **Why use Dynamic Programming for 0/1 Knapsack instead of Greedy?**
   - In 0/1 Knapsack, items are discrete (cannot be cut). A greedy choice based on value/weight ratio can leave empty budget that cannot be filled, leading to suboptimal total value. Dynamic programming evaluates all combinations through subproblems and guarantees the globally optimal choice.

2. **Why does Fractional Knapsack achieve greater or equal value than 0/1 Knapsack?**
   - Fractional Knapsack can take partial fractions of items to completely exhaust the remaining budget with the highest possible value per rupee. Since it is a relaxation of 0/1 Knapsack, its value is always $\ge$ 0/1 Knapsack.

3. **What is the recurrence relation for Merge Sort?**
   - $T(n) = 2T(n/2) + O(n)$. By Master Theorem (Case 2), $T(n) = O(n \log n)$ in best, average, and worst cases.

4. **Why must the list be sorted before Binary Search?**
   - Binary Search requires the elements to be in sorted order so that comparing the target with the middle element (`mid`) reliably tells whether the target lies in the left half or the right half.
