# Smart Budget and Shopping Optimizer

**MCA (Cloud Computing and DevOps) — Design and Analysis of Algorithms (DAA) Mini Project**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-indigo.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Visuals](https://img.shields.io/badge/Data%20Viz-Matplotlib-teal.svg)](https://matplotlib.org/)
[![Database](https://img.shields.io/badge/Storage-Zero--DB%20CSV-green.svg)](https://docs.python.org/3/library/csv.html)

---

## 1. Executive Summary & Objective

**Smart Budget and Shopping Optimizer** is an interactive, modern desktop application designed to solve real-world shopping budget allocation problems using foundational algorithms from the **Design and Analysis of Algorithms (DAA)** syllabus.

The application allows users to set a shopping budget and catalog items with prices, categories, and utility priorities. It dynamically computes optimal purchasing decisions, sorts inventory, and searches products using **four core DAA algorithmic paradigms**, implemented completely from scratch without external algorithm libraries:

1. **0/1 Knapsack Problem** via **Dynamic Programming** (Discrete combinatorial optimization).
2. **Fractional Knapsack Problem** via the **Greedy Method** (Continuous relaxation with ratio ranking).
3. **Merge Sort** via **Divide and Conquer** (Deterministic $O(n \log n)$ stable sorting).
4. **Binary Search** via **Decrease and Conquer** (Logarithmic $O(\log n)$ exact and range searching).

---

## 2. DAA Algorithmic Architecture & Mathematical Formulations

### A. 0/1 Knapsack — Dynamic Programming
* **Problem Statement**: Given a shopping budget $W$ and $n$ products where product $i$ has cost $w_i$ and priority value $v_i$, select a subset of items to maximize total value $\sum_{i=1}^n v_i \cdot x_i$ subject to $\sum_{i=1}^n w_i \cdot x_i \le W$, where $x_i \in \{0, 1\}$.
* **DAA Paradigm**: Dynamic Programming (Bottom-Up Tabulation with Backtracking).
* **Recurrence Relation (Bellman's Equation)**:
  $$K[i, w] = \begin{cases} 
  0 & \text{if } i = 0 \text{ or } w = 0 \\
  K[i - 1, w] & \text{if } w_i > w \\
  \max\Big(K[i - 1, w], \; v_i + K[i - 1, w - w_i]\Big) & \text{if } w_i \le w 
  \end{cases}$$
* **Time Complexity**: $\mathcal{O}(n \times W)$ (Pseudo-polynomial time).
* **Space Complexity**: $\mathcal{O}(n \times W)$ (Auxiliary DP tabulation matrix).
* **Guaranteed Property**: Global optimality for indivisible products.

---

### B. Fractional Knapsack — Greedy Method
* **Problem Statement**: Items can be divided into continuous fractions $x_i \in [0, 1]$.
* **DAA Paradigm**: Greedy Method (Greedy Choice Property & Optimal Substructure).
* **Greedy Selection Metric**: Value-to-Price Ratio:
  $$r_i = \frac{v_i}{w_i} = \frac{\text{Priority}_i}{\text{Price}_i}$$
* **Handling Divisibility**:
  - **Divisible Goods** (e.g. coffee beans, dry fruits, grocery bulk items): Can take a fraction $x_i = \frac{\text{Remaining Budget}}{w_i}$.
  - **Indivisible Goods** (e.g. electronics, accessories): Taken completely ($x_i = 1$) if $w_i \le \text{Remaining Budget}$, else skipped.
* **Time Complexity**: $\mathcal{O}(n \log n)$ (Dominated by ratio sorting).
* **Space Complexity**: $\mathcal{O}(n)$ (To store greedy decisions and ratios).
* **Theoretical Upper Bound**: $\text{Optimal Value}_{\text{Fractional}} \ge \text{Optimal Value}_{0/1}$.

---

### C. Merge Sort — Divide and Conquer
* **Problem Statement**: Sort products by arbitrary attributes (Price, Priority, Name) without using Python's built-in `sort()` or `sorted()`.
* **DAA Paradigm**: Divide and Conquer.
  1. **Divide**: Split array into two halves at $mid = \lfloor \frac{low + high}{2} \rfloor$.
  2. **Conquer**: Recursively sort each subarray.
  3. **Combine**: Merge two sorted subarrays in linear $\mathcal{O}(n)$ time.
* **Recurrence Relation**:
  $$T(n) = 2T(n/2) + \Theta(n) \implies T(n) = \Theta(n \log n) \quad \text{(Master Theorem Case 2)}$$
* **Time Complexity**:
  - Best Case: $\mathcal{O}(n \log n)$
  - Average Case: $\mathcal{O}(n \log n)$
  - Worst Case: $\mathcal{O}(n \log n)$
* **Space Complexity**: $\mathcal{O}(n)$ (Auxiliary buffers for merging).

---

### D. Binary Search — Decrease and Conquer
* **Problem Statement**: Search for products matching an exact price or falling within a price bracket $[P_{\min}, P_{\max}]$.
* **DAA Paradigm**: Decrease and Conquer (Prune-and-Search).
* **Precondition**: The product list **MUST** be sorted by price prior to search (automatically guaranteed using Merge Sort).
* **Recurrence Relation**:
  $$T(n) = T(n/2) + \mathcal{O}(1) \implies T(n) = \mathcal{O}(\log n)$$
* **Time Complexity**:
  - Best Case: $\mathcal{O}(1)$ (Target located at exact midpoint).
  - Average Case: $\mathcal{O}(\log n)$.
  - Worst Case: $\mathcal{O}(\log n)$.
* **Space Complexity**: $\mathcal{O}(1)$ (Iterative implementation).

---

## 3. Algorithm Complexity Reference Matrix

| Algorithm | DAA Paradigm | Best Case | Average Case | Worst Case | Auxiliary Space | Invariant / Guarantee |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **0/1 Knapsack** | Dynamic Programming | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | Global optimum for whole items |
| **Fractional Knapsack** | Greedy Method | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Maximal continuous budget utilization |
| **Merge Sort** | Divide & Conquer | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Stable, deterministic comparison sort |
| **Binary Search** | Decrease & Conquer | $\mathcal{O}(1)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(1)$ | Logarithmic search space bisection |

---

## 4. Project Folder Structure

```text
smart-budget-shopping-optimizer/
│
├── main.py                     # Main Desktop Application entry point & navigation
├── products.csv                # CSV Database for persistent product storage
├── requirements.txt            # Dependency configuration (customtkinter, matplotlib, pillow)
├── test_algorithms.py          # Standalone verification test suite for all 4 algorithms
├── run_app.bat                 # One-click Windows batch launcher
├── README.md                   # Comprehensive project documentation & viva guide
│
├── algorithms/                 # Pure manual DAA Algorithm implementations
│   ├── __init__.py
│   ├── knapsack.py             # 0/1 Knapsack (DP Tabulation & Backtracking)
│   ├── fractional_knapsack.py  # Fractional Knapsack (Greedy Ratio Selection)
│   ├── merge_sort.py           # Merge Sort (Divide & Conquer)
│   └── binary_search.py        # Binary Search (Exact & Range queries)
│
├── gui/                        # Modern Dark-Themed GUI Pages (CustomTkinter)
│   ├── __init__.py
│   ├── dashboard.py            # Page 1: Overview, Stats, Matplotlib category charts
│   ├── product_manager.py      # Page 2: CRUD operations, input validation, CSV sync
│   ├── optimizer.py            # Page 3: 0/1 vs Fractional Knapsack & DP table view
│   ├── search_sort.py          # Page 4: Sorting & Binary Search probe interval visualization
│   └── algorithm_analysis.py   # Page 5: Empirical benchmark curves (Time & Ops vs N)
│
└── utils/                      # Helper modules
    ├── __init__.py
    └── csv_handler.py          # Direct CSV read/write, validation, and auto-seeding
```

---

## 5. Key Features & Application Interface

The desktop UI features a custom dark theme:
* **Background**: Obsidian Charcoal (`#0F111A`) & Navy Slate (`#181A26`)
* **Accents**: Royal Indigo (`#6C5CE7`), Aqua Cyan (`#00CEC9`), Emerald (`#10B981`)
* **Typography**: Clean Segoe UI system fonts with high contrast hierarchy

### Page-by-Page Overview

1. **Dashboard (`gui/dashboard.py`)**:
   - Live KPI cards: Total Products, Active Budget, Selected Item Count, Total Expenditure, and Remaining Budget.
   - Quick Budget Control bar with one-click budget presets (Rs. 1,000, Rs. 2,500, Rs. 5,000, Rs. 10,000, Rs. 15,000).
   - Embedded Matplotlib Donut Chart (Category breakdown) and Bar Chart (Value distribution by category).

2. **Product Management (`gui/product_manager.py`)**:
   - Modern `ttk.Treeview` product catalog with instant search filtering and category dropdowns.
   - Add, Edit, and Delete forms with strict validation:
     - Rejects empty product names or IDs.
     - Prevents duplicate product IDs.
     - Enforces positive numeric prices and valid priority scores (1 to 100).
     - Checkbox/switch for indivisible vs. divisible items.
   - Real-time two-way synchronization with `products.csv`.

3. **Budget Optimizer (`gui/optimizer.py`)**:
   - Side-by-side comparison cards for 0/1 Knapsack vs Fractional Knapsack.
   - Interactive 0/1 Knapsack tab displaying selected whole items and a sampled Dynamic Programming subproblem matrix ($K[i, w]$).
   - Fractional Knapsack tab showing ratio computations ($V/W$), fraction percentages, and a step-by-step greedy decision log.
   - Comparative evaluation tab breaking down differences in budget utilization, speed, and optimality guarantees.

4. **Sorting and Searching (`gui/search_sort.py`)**:
   - **Merge Sort Panel**: Sort by Price, Priority, or Name in Ascending or Descending order with comparison counters and execution timers.
   - **Binary Search Panel**: Search by exact price or price range ($[P_{\min}, P_{\max}]$) with a step-by-step probe log tracing $[low, mid, high]$ intervals.

5. **Algorithm Analysis (`gui/algorithm_analysis.py`)**:
   - Theoretical Complexity Reference Table.
   - Live "Run Empirical Benchmark" button that benchmarks synthetic catalogs of sizes $N \in [15, 30, 60, 120, 240, 480]$ and plots real-time Matplotlib curves:
     1. Execution Time (ms) vs. Input Size $N$.
     2. Operations / Comparisons vs. Input Size $N$.

---

## 6. Installation & Execution Guide

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed.

### Step 1: Install Required Libraries
Open a terminal in the project directory and run:
```bash
pip install -r requirements.txt
```
*(Dependencies: `customtkinter`, `matplotlib`, `pillow`)*

### Step 2: Run Algorithmic Unit Tests
Verify all 4 algorithms and CSV operations before launching the GUI:
```bash
python test_algorithms.py
```

### Step 3: Launch the Desktop Application
Run via Python:
```bash
python main.py
```
Or double-click `run_app.bat` on Windows.

---

## 7. College Viva Voce / Oral Examination Preparation Guide

Use this section to prepare for common questions asked by university professors and external examiners:

### Q1: What is the fundamental difference between the Greedy Approach and Dynamic Programming?
* **Answer**:
  - The **Greedy Approach** makes the locally optimal choice at each step without ever reconsidering past decisions. It requires the *Greedy Choice Property* to achieve a global optimum.
  - **Dynamic Programming** systematically explores all subproblem combinations, stores optimal solutions in a table (memoization/tabulation), and ensures global optimality via *Bellman's Principle of Optimality*.

### Q2: Why does the Greedy Method fail on the 0/1 Knapsack Problem?
* **Answer**:
  In 0/1 Knapsack, items cannot be divided. An item with a high value-to-weight ratio might leave unused, unfillable capacity in the knapsack. A combination of slightly lower-ratio items might fill the budget completely and yield a higher total value.
  *Example*: Capacity $W = 5$. Item 1: $(v=10, w=3, \text{ratio}=3.33)$, Item 2: $(v=7, w=2, \text{ratio}=3.5)$, Item 3: $(v=7, w=3, \text{ratio}=2.33)$.
  Greedy picks Item 2 ($w=2, \text{left}=3$), then cannot pick Item 1 or 3 completely $\implies \text{Total Value} = 7$.
  DP picks Items 2 and 1 ($w=2+3=5$) $\implies \text{Total Value} = 17$.

### Q3: Why is 0/1 Knapsack considered "Pseudo-Polynomial" time?
* **Answer**:
  The time complexity is $\mathcal{O}(n \cdot W)$. While this appears polynomial, $W$ is the numeric value of the budget, which is represented in $\log_2(W)$ bits in binary. An algorithm is truly polynomial only if its runtime is polynomial in the length of the input bits. Since $\mathcal{O}(n \cdot 2^b)$ is exponential with respect to the bit length $b$, it is classified as *pseudo-polynomial*.

### Q4: Why is Merge Sort preferred over QuickSort when worst-case guarantee is required?
* **Answer**:
  Merge Sort guarantees $\mathcal{O}(n \log n)$ time in the worst case, whereas standard QuickSort degrades to $\mathcal{O}(n^2)$ if the pivot choices are poor (e.g. already sorted inputs with naive pivot selection). Furthermore, Merge Sort is a **stable sort**, preserving the relative order of items with equal keys.

### Q5: Why must the list be sorted before running Binary Search?
* **Answer**:
  Binary Search relies on the invariant that elements in the left partition are $\le$ the midpoint value and elements in the right partition are $\ge$ the midpoint value. If the array is unsorted, discarding half the search space could eliminate the target element, causing the algorithm to fail.

---

## 8. License & Academic Attribution
Developed for the **Master of Computer Applications (MCA - Cloud Computing & DevOps)** academic curriculum under the **Design and Analysis of Algorithms (DAA)** laboratory practicals.
