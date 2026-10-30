"""
Algorithm Analysis Page for Smart Budget and Shopping Optimizer.
Visualizes Time and Space Complexities, operations metrics,
and live empirical benchmark graphs using Matplotlib.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import time
import random
from typing import Dict, Any, List
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms.knapsack import ZeroOneKnapsack
from algorithms.fractional_knapsack import FractionalKnapsack
from algorithms.merge_sort import MergeSort
from algorithms.binary_search import BinarySearch


class AlgorithmAnalysisPage(ctk.CTkFrame):
    """
    Theoretical and empirical algorithm analysis dashboard
    providing complexity analysis, operation counting, and live benchmarks.
    """

    COMPLEXITY_DATA = [
        {
            "name": "0/1 Knapsack",
            "paradigm": "Dynamic Programming",
            "best": "O(n * W)",
            "avg": "O(n * W)",
            "worst": "O(n * W)",
            "space": "O(n * W)",
            "description": "Explores optimal substructure via bottom-up tabulation matrix. Pseudo-polynomial time."
        },
        {
            "name": "Fractional Knapsack",
            "paradigm": "Greedy Method",
            "best": "O(n log n)",
            "avg": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)",
            "description": "Ranks items by value-to-price ratio (v/w) using Merge Sort, then takes whole or fractional items."
        },
        {
            "name": "Merge Sort",
            "paradigm": "Divide and Conquer",
            "best": "O(n log n)",
            "avg": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)",
            "description": "Recursively bisects array, sorts halves, and merges linearly. Stable and deterministic."
        },
        {
            "name": "Binary Search",
            "paradigm": "Decrease and Conquer",
            "best": "O(1)",
            "avg": "O(log n)",
            "worst": "O(log n)",
            "space": "O(1)",
            "description": "Repeatedly halves search interval on sorted data. Preconditioned on sorted ordering."
        }
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_ui()
        self.run_benchmark()

    def _build_ui(self):
        # Header Row
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Algorithm Complexity & Empirical Analysis",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text="DAA Syllabus Performance Evaluation & Complexity Curves",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF"
        ).pack(side="left", padx=15, pady=(5, 0))

        ctk.CTkButton(
            header_frame,
            text="⚡ Run Empirical Benchmark",
            command=self.run_benchmark,
            fg_color="#6C5CE7",
            hover_color="#5848C2",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            width=200
        ).pack(side="right")

        # Top Section: Theoretical Complexity Table
        tbl_card = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        tbl_card.pack(fill="x", padx=25, pady=(0, 10))

        tbl_hdr = ctk.CTkFrame(tbl_card, fg_color="transparent")
        tbl_hdr.pack(fill="x", padx=15, pady=(10, 4))

        ctk.CTkLabel(
            tbl_hdr,
            text="DAA Syllabus Theoretical Complexity Matrix",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        cols = ("name", "paradigm", "best", "avg", "worst", "space", "desc")
        self.tree = ttk.Treeview(tbl_card, columns=cols, show="headings", style="ProductTree.Treeview", height=4)
        self.tree.heading("name", text="Algorithm Name")
        self.tree.heading("paradigm", text="DAA Paradigm")
        self.tree.heading("best", text="Best Case")
        self.tree.heading("avg", text="Average Case")
        self.tree.heading("worst", text="Worst Case")
        self.tree.heading("space", text="Auxiliary Space")
        self.tree.heading("desc", text="Working Mechanism & Invariant")

        self.tree.column("name", width=140, anchor="w")
        self.tree.column("paradigm", width=150, anchor="w")
        self.tree.column("best", width=85, anchor="center")
        self.tree.column("avg", width=95, anchor="center")
        self.tree.column("worst", width=85, anchor="center")
        self.tree.column("space", width=105, anchor="center")
        self.tree.column("desc", width=340, anchor="w")

        for item in self.COMPLEXITY_DATA:
            self.tree.insert("", "end", values=(
                item["name"], item["paradigm"], item["best"], item["avg"], item["worst"], item["space"], item["description"]
            ))

        self.tree.pack(fill="x", padx=12, pady=(0, 10))

        # Bottom Section: Matplotlib Benchmark Curves
        chart_card = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        chart_card.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        chart_hdr = ctk.CTkFrame(chart_card, fg_color="transparent")
        chart_hdr.pack(fill="x", padx=15, pady=(10, 2))

        ctk.CTkLabel(
            chart_hdr,
            text="Empirical Benchmark Graphs (Execution Time & Operations Count vs. Input Size N)",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#00CEC9"
        ).pack(side="left")

        self.benchmark_status = ctk.CTkLabel(
            chart_hdr,
            text="Ready",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9CA3AF"
        )
        self.benchmark_status.pack(side="right")

        self.chart_container = ctk.CTkFrame(chart_card, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=12, pady=(0, 10))

    def run_benchmark(self):
        """Generates synthetic datasets of varying sizes and measures real runtime."""
        self.benchmark_status.configure(text="Benchmarking in progress...", text_color="#FDCB6E")
        self.update_idletasks()

        sizes = [15, 30, 60, 120, 240, 480]

        time_01_knapsack = []
        time_frac_knapsack = []
        time_merge_sort = []
        time_binary_search = []

        ops_merge_sort = []
        ops_binary_search = []
        ops_dp = []

        fixed_budget = 3000
        sorter = MergeSort()

        # Deterministic seed for reproducible evaluation curves
        rng = random.Random(42)

        for n in sizes:
            # Generate n random products
            sample_prods = []
            for i in range(n):
                sample_prods.append({
                    "product_id": f"P{i+1:04d}",
                    "product_name": f"Sample Item {i+1}",
                    "category": rng.choice(["Electronics", "Accessories", "Stationery", "Daily Essentials"]),
                    "price": rng.randint(100, 2500),
                    "priority": rng.randint(1, 10),
                    "is_divisible": rng.choice([0, 1])
                })

            # 1. 0/1 Knapsack
            t0 = time.perf_counter()
            dp_res = ZeroOneKnapsack.solve(sample_prods, fixed_budget)
            t_dp = (time.perf_counter() - t0) * 1000.0
            time_01_knapsack.append(t_dp)
            ops_dp.append(dp_res["operations_count"])

            # 2. Fractional Knapsack
            t0 = time.perf_counter()
            FractionalKnapsack.solve(sample_prods, fixed_budget)
            t_gr = (time.perf_counter() - t0) * 1000.0
            time_frac_knapsack.append(t_gr)

            # 3. Merge Sort
            sorted_prods, comps, t_ms, _ = sorter.sort(sample_prods, key="price", ascending=True)
            time_merge_sort.append(t_ms)
            ops_merge_sort.append(comps)

            # 4. Binary Search
            mid_val = sorted_prods[n // 2]["price"]
            t0 = time.perf_counter()
            bs_res = BinarySearch.search_by_exact_price(sorted_prods, mid_val)
            t_bs = (time.perf_counter() - t0) * 1000.0
            time_binary_search.append(t_bs)
            ops_binary_search.append(bs_res["comparisons"])

        self._render_charts(
            sizes,
            time_01_knapsack,
            time_frac_knapsack,
            time_merge_sort,
            time_binary_search,
            ops_merge_sort,
            ops_binary_search,
            ops_dp
        )
        self.benchmark_status.configure(text=f"Benchmark completed successfully ({len(sizes)} test points).", text_color="#10B981")

    def _render_charts(self, sizes, t_dp, t_gr, t_ms, t_bs, ops_ms, ops_bs, ops_dp):
        for child in self.chart_container.winfo_children():
            child.destroy()

        fig = Figure(figsize=(9.2, 3.8), dpi=100, facecolor="#1F2233")
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Chart 1: Execution Time (ms) vs Input Size N
        ax1.set_facecolor("#181A26")
        ax1.plot(sizes, t_dp, marker="o", color="#A29BFE", linewidth=2, label="0/1 Knapsack (DP)")
        ax1.plot(sizes, t_gr, marker="s", color="#00CEC9", linewidth=2, label="Fractional Knapsack (Greedy)")
        ax1.plot(sizes, t_ms, marker="^", color="#FDCB6E", linewidth=2, label="Merge Sort (O(n log n))")
        ax1.plot(sizes, t_bs, marker="d", color="#FF7675", linewidth=2, label="Binary Search (O(log n))")

        ax1.set_title("Execution Time (ms) vs. Number of Products (N)", color="#F3F4F6", fontsize=10, weight="bold", pad=8)
        ax1.set_xlabel("Number of Products (N)", color="#CBD5E1", fontsize=9)
        ax1.set_ylabel("Execution Time (milliseconds)", color="#CBD5E1", fontsize=9)
        ax1.tick_params(colors="#9CA3AF", labelsize=8)
        ax1.spines["bottom"].set_color("#2C3048")
        ax1.spines["left"].set_color("#2C3048")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.grid(True, linestyle="--", alpha=0.25, color="#4A5568")
        ax1.legend(loc="upper left", fontsize=7.5, facecolor="#1F2233", edgecolor="#2C3048", labelcolor="#E2E8F0")

        # Chart 2: Operations Count vs Input Size N
        ax2.set_facecolor("#181A26")
        ax2.plot(sizes, ops_ms, marker="^", color="#FDCB6E", linewidth=2, label="Merge Sort Comparisons")
        ax2.plot(sizes, ops_bs, marker="d", color="#FF7675", linewidth=2, label="Binary Search Comparisons")

        ax2.set_title("Algorithm Operations / Comparisons vs. N", color="#F3F4F6", fontsize=10, weight="bold", pad=8)
        ax2.set_xlabel("Number of Products (N)", color="#CBD5E1", fontsize=9)
        ax2.set_ylabel("Comparison Operations", color="#CBD5E1", fontsize=9)
        ax2.tick_params(colors="#9CA3AF", labelsize=8)
        ax2.spines["bottom"].set_color("#2C3048")
        ax2.spines["left"].set_color("#2C3048")
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.grid(True, linestyle="--", alpha=0.25, color="#4A5568")
        ax2.legend(loc="upper left", fontsize=7.5, facecolor="#1F2233", edgecolor="#2C3048", labelcolor="#E2E8F0")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
