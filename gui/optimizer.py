"""
Budget Optimizer Page for Smart Budget and Shopping Optimizer.
Implements dynamic visual comparison between 0/1 Knapsack (DP)
and Fractional Knapsack (Greedy Method).
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List, Callable
from algorithms.knapsack import ZeroOneKnapsack
from algorithms.fractional_knapsack import FractionalKnapsack


class BudgetOptimizerPage(ctk.CTkFrame):
    """
    Budget Optimizer Workspace comparing Dynamic Programming (0/1 Knapsack)
    against the Greedy Method (Fractional Knapsack) with subproblem visualization.
    """

    def __init__(self, master, get_products: Callable[[], List[Dict[str, Any]]], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.get_products = get_products
        self.current_budget = 5000

        self._build_ui()
        self.run_optimization()

    def _build_ui(self):
        # Header Row
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Algorithmic Budget Optimizer",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text="DAA Syllabus: 0/1 Knapsack (DP) vs. Fractional Knapsack (Greedy)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF"
        ).pack(side="left", padx=15, pady=(5, 0))

        # Control Panel (Budget Input & Presets)
        ctrl_bar = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        ctrl_bar.pack(fill="x", padx=25, pady=8)

        ctk.CTkLabel(
            ctrl_bar,
            text="Shopping Budget:",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left", padx=(18, 10), pady=12)

        self.budget_entry = ctk.CTkEntry(
            ctrl_bar,
            placeholder_text="Enter budget (Rs.)",
            width=130,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        self.budget_entry.insert(0, str(self.current_budget))
        self.budget_entry.pack(side="left", padx=5, pady=12)

        self.optimize_btn = ctk.CTkButton(
            ctrl_bar,
            text="⚡ Run DAA Optimization",
            command=self.run_optimization,
            fg_color="#6C5CE7",
            hover_color="#5848C2",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            width=190
        )
        self.optimize_btn.pack(side="left", padx=12, pady=12)

        # Budget presets
        ctk.CTkLabel(
            ctrl_bar,
            text="Presets:",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9CA3AF"
        ).pack(side="left", padx=(15, 6), pady=12)

        for p in [1500, 3000, 5000, 7500, 10000]:
            ctk.CTkButton(
                ctrl_bar,
                text=f"Rs. {p:,}",
                command=lambda val=p: self._set_budget_preset(val),
                width=75,
                height=28,
                fg_color="#2B2E42",
                hover_color="#3D405B",
                font=ctk.CTkFont(family="Segoe UI", size=11)
            ).pack(side="left", padx=3, pady=12)

        # High-level Comparative Metrics Banner
        self.comp_banner = ctk.CTkFrame(self, fg_color="transparent")
        self.comp_banner.pack(fill="x", padx=20, pady=5)
        self.comp_banner.grid_columnconfigure((0, 1), weight=1, uniform="comp_cards")

        # DP Summary Card
        self.card_dp = ctk.CTkFrame(self.comp_banner, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#6C5CE7")
        self.card_dp.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        dp_hdr = ctk.CTkFrame(self.card_dp, fg_color="transparent")
        dp_hdr.pack(fill="x", padx=15, pady=(10, 4))
        ctk.CTkLabel(dp_hdr, text="0/1 Knapsack (Dynamic Programming)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#A29BFE").pack(side="left")
        ctk.CTkLabel(dp_hdr, text="Whole Items Only", font=ctk.CTkFont(size=11), text_color="#CBD5E1").pack(side="right")

        self.dp_stats_label = ctk.CTkLabel(
            self.card_dp,
            text="Cost: Rs. 0 | Value: 0 | Items: 0 | Remaining: Rs. 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#F3F4F6"
        )
        self.dp_stats_label.pack(anchor="w", padx=15, pady=(2, 10))

        # Greedy Summary Card
        self.card_greedy = ctk.CTkFrame(self.comp_banner, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#00CEC9")
        self.card_greedy.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        gr_hdr = ctk.CTkFrame(self.card_greedy, fg_color="transparent")
        gr_hdr.pack(fill="x", padx=15, pady=(10, 4))
        ctk.CTkLabel(gr_hdr, text="Fractional Knapsack (Greedy Approach)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00CEC9").pack(side="left")
        ctk.CTkLabel(gr_hdr, text="Allows Divisible Goods", font=ctk.CTkFont(size=11), text_color="#CBD5E1").pack(side="right")

        self.greedy_stats_label = ctk.CTkLabel(
            self.card_greedy,
            text="Cost: Rs. 0 | Value: 0 | Items: 0 | Remaining: Rs. 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#F3F4F6"
        )
        self.greedy_stats_label.pack(anchor="w", padx=15, pady=(2, 10))

        # Main Tabview for Detailed Algorithm Deep-Dives
        self.tabview = ctk.CTkTabview(
            self,
            fg_color="#1F2233",
            segmented_button_fg_color="#181A26",
            segmented_button_selected_color="#6C5CE7",
            segmented_button_selected_hover_color="#5848C2",
            segmented_button_unselected_color="#2B2E42",
            segmented_button_unselected_hover_color="#3D405B"
        )
        self.tabview.pack(fill="both", expand=True, padx=25, pady=(5, 15))

        self.tab_dp = self.tabview.add("0/1 Knapsack (DP Results)")
        self.tab_greedy = self.tabview.add("Fractional Knapsack (Greedy Results)")
        self.tab_comparison = self.tabview.add("Side-by-Side Comparison & Viva Notes")

        self._build_dp_tab()
        self._build_greedy_tab()
        self._build_comparison_tab()

    def _set_budget_preset(self, amount: int):
        self.current_budget = amount
        self.budget_entry.delete(0, "end")
        self.budget_entry.insert(0, str(amount))
        self.run_optimization()

    def _build_dp_tab(self):
        # Split: Left Selected Items Table, Right DP Table Visualizer
        dp_frame = ctk.CTkFrame(self.tab_dp, fg_color="transparent")
        dp_frame.pack(fill="both", expand=True, padx=5, pady=5)
        dp_frame.grid_columnconfigure(0, weight=3)
        dp_frame.grid_columnconfigure(1, weight=2)
        dp_frame.grid_rowconfigure(0, weight=1)

        # Left: Selected Products Table
        left_box = ctk.CTkFrame(dp_frame, fg_color="#181A26", corner_radius=10)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=5)

        ctk.CTkLabel(
            left_box,
            text="Selected Products (Whole Items - 0/1 Selection)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#A29BFE"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        tree_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("id", "name", "category", "price", "priority")
        self.dp_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", style="ProductTree.Treeview", height=10)
        self.dp_tree.heading("id", text="ID")
        self.dp_tree.heading("name", text="Product Name")
        self.dp_tree.heading("category", text="Category")
        self.dp_tree.heading("price", text="Price (Rs.)")
        self.dp_tree.heading("priority", text="Priority")

        self.dp_tree.column("id", width=60, anchor="center")
        self.dp_tree.column("name", width=190, anchor="w")
        self.dp_tree.column("category", width=120, anchor="w")
        self.dp_tree.column("price", width=85, anchor="e")
        self.dp_tree.column("priority", width=70, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.dp_tree.yview)
        self.dp_tree.configure(yscrollcommand=scroll.set)
        self.dp_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Right: DP Table Visualization & Explanation
        right_box = ctk.CTkFrame(dp_frame, fg_color="#181A26", corner_radius=10)
        right_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=5)

        ctk.CTkLabel(
            right_box,
            text="Dynamic Programming Table Sample (Subproblems K[i, w])",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00CEC9"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        # Sampled DP Table Text Box
        self.dp_table_box = ctk.CTkTextbox(
            right_box,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color="#12131C",
            text_color="#E2E8F0",
            wrap="none"
        )
        self.dp_table_box.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # Explanation box at bottom
        self.dp_explanation_label = ctk.CTkLabel(
            right_box,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#CBD5E1",
            justify="left",
            wraplength=340
        )
        self.dp_explanation_label.pack(anchor="w", padx=15, pady=(0, 10))

    def _build_greedy_tab(self):
        gr_frame = ctk.CTkFrame(self.tab_greedy, fg_color="transparent")
        gr_frame.pack(fill="both", expand=True, padx=5, pady=5)
        gr_frame.grid_columnconfigure(0, weight=3)
        gr_frame.grid_columnconfigure(1, weight=2)
        gr_frame.grid_rowconfigure(0, weight=1)

        # Left: Selected Products Table with Quantities/Fractions
        left_box = ctk.CTkFrame(gr_frame, fg_color="#181A26", corner_radius=10)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=5)

        ctk.CTkLabel(
            left_box,
            text="Greedy Selection (Ranked by Value-to-Price Ratio)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00CEC9"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        tree_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("name", "ratio", "fraction", "paid_cost", "earned_value")
        self.greedy_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", style="ProductTree.Treeview", height=10)
        self.greedy_tree.heading("name", text="Product Name")
        self.greedy_tree.heading("ratio", text="Ratio (V/Rs)")
        self.greedy_tree.heading("fraction", text="Portion Taken")
        self.greedy_tree.heading("paid_cost", text="Paid Cost (Rs.)")
        self.greedy_tree.heading("earned_value", text="Earned Value")

        self.greedy_tree.column("name", width=180, anchor="w")
        self.greedy_tree.column("ratio", width=90, anchor="center")
        self.greedy_tree.column("fraction", width=95, anchor="center")
        self.greedy_tree.column("paid_cost", width=95, anchor="e")
        self.greedy_tree.column("earned_value", width=90, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.greedy_tree.yview)
        self.greedy_tree.configure(yscrollcommand=scroll.set)
        self.greedy_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Right: Greedy Step Decision Log
        right_box = ctk.CTkFrame(gr_frame, fg_color="#181A26", corner_radius=10)
        right_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=5)

        ctk.CTkLabel(
            right_box,
            text="Greedy Decision Trace Log",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FDCB6E"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.greedy_trace_box = ctk.CTkTextbox(
            right_box,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color="#12131C",
            text_color="#E2E8F0",
            wrap="none"
        )
        self.greedy_trace_box.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.greedy_explanation_label = ctk.CTkLabel(
            right_box,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#CBD5E1",
            justify="left",
            wraplength=340
        )
        self.greedy_explanation_label.pack(anchor="w", padx=15, pady=(0, 10))

    def _build_comparison_tab(self):
        comp_frame = ctk.CTkFrame(self.tab_comparison, fg_color="transparent")
        comp_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Comparative Table
        ctk.CTkLabel(
            comp_frame,
            text="Dynamic Programming vs. Greedy Method: Side-by-Side Analysis",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w", pady=(0, 8))

        tbl_container = ctk.CTkFrame(comp_frame, fg_color="#181A26", corner_radius=10)
        tbl_container.pack(fill="x", pady=(0, 12))

        cols = ("attribute", "dp_val", "greedy_val", "difference")
        self.comp_tree = ttk.Treeview(tbl_container, columns=cols, show="headings", style="ProductTree.Treeview", height=7)
        self.comp_tree.heading("attribute", text="Optimization Metric")
        self.comp_tree.heading("dp_val", text="0/1 Knapsack (DP)")
        self.comp_tree.heading("greedy_val", text="Fractional Knapsack (Greedy)")
        self.comp_tree.heading("difference", text="Comparative Observation")

        self.comp_tree.column("attribute", width=220, anchor="w")
        self.comp_tree.column("dp_val", width=180, anchor="center")
        self.comp_tree.column("greedy_val", width=180, anchor="center")
        self.comp_tree.column("difference", width=280, anchor="w")

        self.comp_tree.pack(fill="x", padx=10, pady=10)

        # Viva Concept Explanation Panel
        viva_container = ctk.CTkFrame(comp_frame, fg_color="#181A26", corner_radius=10)
        viva_container.pack(fill="both", expand=True, pady=(0, 5))

        ctk.CTkLabel(
            viva_container,
            text="🎓 DAA Viva Voce Key Points: Why does Greedy fail on 0/1 Knapsack?",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00CEC9"
        ).pack(anchor="w", padx=15, pady=(12, 6))

        viva_text = (
            "1. Greedy Choice Property:\n"
            "   - In Fractional Knapsack, selecting items strictly by highest Value/Price ratio (v_i / w_i) is mathematically proven to be globally optimal.\n"
            "   - In 0/1 Knapsack, items cannot be broken. A high ratio item might leave wasted, unfillable capacity, whereas a combination of slightly lower ratio items might fill the budget completely and yield higher total value.\n\n"
            "2. Dynamic Programming Optimal Substructure:\n"
            "   - 0/1 Knapsack exhibits optimal substructure and overlapping subproblems: K[i, w] = max(K[i-1, w], v_i + K[i-1, w - w_i]).\n"
            "   - Bottom-up tabulation checks all subset combinations systematically in O(n * W) pseudo-polynomial time.\n\n"
            "3. Upper Bound Relationship:\n"
            "   - Optimal Value (Fractional Knapsack) >= Optimal Value (0/1 Knapsack). Fractional Knapsack is a continuous relaxation of the integer 0/1 problem."
        )

        ctk.CTkLabel(
            viva_container,
            text=viva_text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#CBD5E1",
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 12))

    def run_optimization(self):
        """Executes both 0/1 Knapsack and Fractional Knapsack dynamically."""
        try:
            val = int(float(self.budget_entry.get().strip()))
            if val < 0:
                val = 0
            self.current_budget = val
        except ValueError:
            self.current_budget = 5000

        products = self.get_products()
        if not products:
            return

        # 1. Run 0/1 Knapsack (DP)
        dp_res = ZeroOneKnapsack.solve(products, self.current_budget)
        # 2. Run Fractional Knapsack (Greedy)
        gr_res = FractionalKnapsack.solve(products, self.current_budget)

        # Update Top Comparative Banner
        self.dp_stats_label.configure(
            text=f"Cost: Rs. {dp_res['total_cost']:,}  |  Priority Value: {dp_res['total_value']}  |  "
                 f"Items: {len(dp_res['selected_products'])}  |  Left: Rs. {dp_res['remaining_budget']:,}  |  "
                 f"Time: {dp_res['execution_time_ms']} ms"
        )

        self.greedy_stats_label.configure(
            text=f"Cost: Rs. {gr_res['total_cost']:,}  |  Priority Value: {gr_res['total_value']}  |  "
                 f"Items: {len(gr_res['selected_products'])}  |  Left: Rs. {gr_res['remaining_budget']:,}  |  "
                 f"Time: {gr_res['execution_time_ms']} ms"
        )

        # Populate Tab 1: 0/1 Knapsack Tree
        for r in self.dp_tree.get_children():
            self.dp_tree.delete(r)

        for p in dp_res["selected_products"]:
            self.dp_tree.insert(
                "", "end",
                values=(p["product_id"], p["product_name"], p["category"], f"Rs. {p['price']:,}", p["priority"])
            )

        # Render Sampled DP Table
        self.dp_table_box.delete("1.0", "end")
        sampled_rows = dp_res.get("sampled_dp", [])
        sampled_cols = dp_res.get("sampled_cols", [])

        if sampled_rows and sampled_cols:
            header_str = f"{'Item (Weight)':<24} | " + " | ".join(f"w={c:<5}" for c in sampled_cols) + "\n"
            sep_str = "-" * len(header_str) + "\n"
            self.dp_table_box.insert("end", header_str)
            self.dp_table_box.insert("end", sep_str)

            for row in sampled_rows:
                row_str = f"{row['item_label']:<24} | " + " | ".join(f"{v:<7}" for v in row["values"]) + "\n"
                self.dp_table_box.insert("end", row_str)

        self.dp_explanation_label.configure(text=dp_res["explanation"])

        # Populate Tab 2: Fractional Knapsack Tree & Trace
        for r in self.greedy_tree.get_children():
            self.greedy_tree.delete(r)

        for item in gr_res["selected_products"]:
            frac_str = "100% (Whole)" if item["fraction"] >= 1.0 else f"{round(item['fraction'] * 100, 1)}% (Fractional)"
            self.greedy_tree.insert(
                "", "end",
                values=(
                    item["product_name"],
                    f"{item['ratio']:.5f}",
                    frac_str,
                    f"Rs. {round(item['taken_cost'], 1):,}",
                    f"{round(item['taken_value'], 2)}"
                )
            )

        self.greedy_trace_box.delete("1.0", "end")
        trace_header = f"{'Step':<5} | {'Product Name':<22} | {'Ratio':<8} | {'Decision Action':<26} | {'Rem Budget':<10}\n"
        self.greedy_trace_box.insert("end", trace_header)
        self.greedy_trace_box.insert("end", "-" * len(trace_header) + "\n")

        for idx, dec in enumerate(gr_res["decisions"], 1):
            line = f"{idx:<5} | {dec['product_name'][:20]:<22} | {dec['ratio']:<8.4f} | {dec['action']:<26} | Rs.{dec['remaining_budget']:<8}\n"
            self.greedy_trace_box.insert("end", line)

        self.greedy_explanation_label.configure(text=gr_res["explanation"])

        # Populate Tab 3: Side-by-Side Comparison Treeview
        for r in self.comp_tree.get_children():
            self.comp_tree.delete(r)

        util_dp = round((dp_res['total_cost'] / self.current_budget) * 100, 1) if self.current_budget > 0 else 0
        util_gr = round((gr_res['total_cost'] / self.current_budget) * 100, 1) if self.current_budget > 0 else 0

        rows = [
            ("Algorithmic Paradigm", "Dynamic Programming", "Greedy Method", "DP explores subproblems; Greedy makes irrevocable choices"),
            ("Guaranteed Optimality", "Global Optimum (Whole Items)", "Optimal only for Divisible items", "Greedy cannot guarantee 0/1 optimum"),
            ("Total Priority Value", f"{dp_res['total_value']}", f"{gr_res['total_value']}", f"Greedy achieved +{round(gr_res['total_value'] - dp_res['total_value'], 2)} extra value via fractional parts"),
            ("Total Expenditure", f"Rs. {dp_res['total_cost']:,}", f"Rs. {gr_res['total_cost']:,}", f"Budget utilization: DP {util_dp}% vs Greedy {util_gr}%"),
            ("Remaining Budget", f"Rs. {dp_res['remaining_budget']:,}", f"Rs. {gr_res['remaining_budget']:,}", "Greedy exhausts more budget by taking fractional units"),
            ("Items Selected", f"{len(dp_res['selected_products'])} whole items", f"{len(gr_res['selected_products'])} items (incl. fractions)", "Greedy fills residual gaps with divisible goods"),
            ("Time Complexity", "O(n * W)", "O(n log n)", "Greedy is significantly faster for large capacities W"),
            ("Space Complexity", "O(n * W)", "O(n)", "DP requires a 2D matrix; Greedy requires linear space")
        ]

        for attr, dp_v, gr_v, diff in rows:
            self.comp_tree.insert("", "end", values=(attr, dp_v, gr_v, diff))
