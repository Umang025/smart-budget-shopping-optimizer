"""
Algorithm Analysis Page (Simplified)
Shows DAA theoretical complexities and a live empirical performance graph.
"""

import customtkinter as ctk
from tkinter import ttk
import time
import random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms.knapsack import solve_01_knapsack
from algorithms.fractional_knapsack import solve_fractional_knapsack
from algorithms.merge_sort import merge_sort
from algorithms.binary_search import binary_search_exact


class AlgorithmAnalysisPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_ui()
        self.run_benchmark()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text="Algorithm Analysis & Benchmark",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="⚡ Run Benchmark",
            command=self.run_benchmark,
            fg_color="#6C5CE7",
            width=140
        ).pack(side="right")

        # Theoretical Table
        tbl_frame = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=10)
        tbl_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(tbl_frame, text="DAA Complexity Summary Table", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(8, 4))

        cols = ("name", "paradigm", "time", "space")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=4)
        self.tree.heading("name", text="Algorithm")
        self.tree.heading("paradigm", text="DAA Paradigm")
        self.tree.heading("time", text="Time Complexity")
        self.tree.heading("space", text="Space Complexity")
        self.tree.column("name", width=160)
        self.tree.column("paradigm", width=180)
        self.tree.column("time", width=140, anchor="center")
        self.tree.column("space", width=140, anchor="center")

        data = [
            ("0/1 Knapsack", "Dynamic Programming", "O(n * W)", "O(n * W)"),
            ("Fractional Knapsack", "Greedy Method", "O(n log n)", "O(n)"),
            ("Merge Sort", "Divide and Conquer", "O(n log n)", "O(n)"),
            ("Binary Search", "Decrease and Conquer", "O(log n)", "O(1)")
        ]
        for row in data:
            self.tree.insert("", "end", values=row)

        self.tree.pack(fill="x", padx=10, pady=(0, 10))

        # Chart Frame
        self.chart_frame = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=10)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    def run_benchmark(self):
        for w in self.chart_frame.winfo_children():
            w.destroy()

        sizes = [20, 50, 100, 200, 300]
        t_dp = []
        t_greedy = []
        t_merge = []

        rng = random.Random(42)
        budget = 3000

        for n in sizes:
            items = []
            for i in range(n):
                items.append({
                    "product_id": f"P{i}",
                    "product_name": f"Item {i}",
                    "category": "General",
                    "price": rng.randint(100, 2000),
                    "priority": rng.randint(1, 10),
                    "is_divisible": rng.choice([0, 1])
                })

            # 1. 0/1 Knapsack
            t0 = time.perf_counter()
            solve_01_knapsack(items, budget)
            t_dp.append((time.perf_counter() - t0) * 1000.0)

            # 2. Fractional Knapsack
            t0 = time.perf_counter()
            solve_fractional_knapsack(items, budget)
            t_greedy.append((time.perf_counter() - t0) * 1000.0)

            # 3. Merge Sort
            t0 = time.perf_counter()
            merge_sort(items, key="price", ascending=True)
            t_merge.append((time.perf_counter() - t0) * 1000.0)

        # Plot Matplotlib Graph
        fig = Figure(figsize=(7, 3.2), dpi=100, facecolor="#1F2233")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#181A26")

        ax.plot(sizes, t_dp, marker="o", color="#A29BFE", label="0/1 Knapsack (DP)")
        ax.plot(sizes, t_greedy, marker="s", color="#00CEC9", label="Fractional Knapsack (Greedy)")
        ax.plot(sizes, t_merge, marker="^", color="#FDCB6E", label="Merge Sort (O(n log n))")

        ax.set_title("Empirical Execution Time vs. Input Size (N)", color="#F3F4F6", fontsize=11, weight="bold")
        ax.set_xlabel("Number of Products (N)", color="#CBD5E1", fontsize=9)
        ax.set_ylabel("Execution Time (ms)", color="#CBD5E1", fontsize=9)
        ax.tick_params(colors="#CBD5E1", labelsize=8)
        ax.grid(True, linestyle="--", alpha=0.3, color="#4A5568")
        ax.legend(facecolor="#1F2233", edgecolor="#2C3048", labelcolor="#F3F4F6", fontsize=8)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
