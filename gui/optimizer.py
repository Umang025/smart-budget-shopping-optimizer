"""
Budget Optimizer Page (Simplified)
Compares 0/1 Knapsack (Dynamic Programming) and Fractional Knapsack (Greedy).
"""

import customtkinter as ctk
from tkinter import ttk
from typing import Dict, Any, List, Callable
from algorithms.knapsack import solve_01_knapsack
from algorithms.fractional_knapsack import solve_fractional_knapsack


class BudgetOptimizerPage(ctk.CTkFrame):
    def __init__(self, master, get_products: Callable[[], List[Dict[str, Any]]], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.get_products = get_products
        self.current_budget = 5000

        self._build_ui()
        self.optimize()

    def _build_ui(self):
        # Header & Controls
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text="Budget Optimizer (DP vs. Greedy)",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        # Top Control Bar
        ctrl_bar = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=10)
        ctrl_bar.pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(ctrl_bar, text="Budget (Rs.):", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=12, pady=10)

        self.budget_entry = ctk.CTkEntry(ctrl_bar, width=120)
        self.budget_entry.insert(0, str(self.current_budget))
        self.budget_entry.pack(side="left", padx=5, pady=10)

        ctk.CTkButton(
            ctrl_bar,
            text="⚡ Run Optimization",
            command=self.optimize,
            fg_color="#6C5CE7",
            hover_color="#5848C2",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=10, pady=10)

        # Preset Buttons
        for p in [2500, 5000, 7500, 10000]:
            ctk.CTkButton(
                ctrl_bar,
                text=f"Rs.{p:,}",
                command=lambda val=p: self._set_budget(val),
                width=75,
                fg_color="#2B2E42"
            ).pack(side="left", padx=3, pady=10)

        # Side-by-Side Results Container
        results_container = ctk.CTkFrame(self, fg_color="transparent")
        results_container.pack(fill="both", expand=True, padx=20, pady=5)
        results_container.grid_columnconfigure((0, 1), weight=1)
        results_container.grid_rowconfigure(0, weight=1)

        # Left Column: 0/1 Knapsack (DP)
        dp_box = ctk.CTkFrame(results_container, fg_color="#1F2233", corner_radius=10)
        dp_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        ctk.CTkLabel(
            dp_box,
            text="1. 0/1 Knapsack (Dynamic Programming)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#A29BFE"
        ).pack(anchor="w", padx=12, pady=(10, 2))

        self.dp_summary_lbl = ctk.CTkLabel(dp_box, text="", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00CEC9")
        self.dp_summary_lbl.pack(anchor="w", padx=12, pady=(0, 5))

        tree1_frame = ctk.CTkFrame(dp_box, fg_color="transparent")
        tree1_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols1 = ("name", "category", "price", "priority")
        self.dp_tree = ttk.Treeview(tree1_frame, columns=cols1, show="headings", height=8)
        self.dp_tree.heading("name", text="Product Name")
        self.dp_tree.heading("category", text="Category")
        self.dp_tree.heading("price", text="Price (Rs.)")
        self.dp_tree.heading("priority", text="Priority")
        self.dp_tree.column("name", width=160)
        self.dp_tree.column("category", width=100)
        self.dp_tree.column("price", width=75, anchor="e")
        self.dp_tree.column("priority", width=60, anchor="center")

        scroll1 = ttk.Scrollbar(tree1_frame, orient="vertical", command=self.dp_tree.yview)
        self.dp_tree.configure(yscrollcommand=scroll1.set)
        self.dp_tree.pack(side="left", fill="both", expand=True)
        scroll1.pack(side="right", fill="y")

        # Right Column: Fractional Knapsack (Greedy)
        greedy_box = ctk.CTkFrame(results_container, fg_color="#1F2233", corner_radius=10)
        greedy_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        ctk.CTkLabel(
            greedy_box,
            text="2. Fractional Knapsack (Greedy Method)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00CEC9"
        ).pack(anchor="w", padx=12, pady=(10, 2))

        self.greedy_summary_lbl = ctk.CTkLabel(greedy_box, text="", font=ctk.CTkFont(size=11, weight="bold"), text_color="#FDCB6E")
        self.greedy_summary_lbl.pack(anchor="w", padx=12, pady=(0, 5))

        tree2_frame = ctk.CTkFrame(greedy_box, fg_color="transparent")
        tree2_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols2 = ("name", "quantity", "cost", "value")
        self.greedy_tree = ttk.Treeview(tree2_frame, columns=cols2, show="headings", height=8)
        self.greedy_tree.heading("name", text="Product Name")
        self.greedy_tree.heading("quantity", text="Portion")
        self.greedy_tree.heading("cost", text="Cost (Rs.)")
        self.greedy_tree.heading("value", text="Value")
        self.greedy_tree.column("name", width=160)
        self.greedy_tree.column("quantity", width=80, anchor="center")
        self.greedy_tree.column("cost", width=80, anchor="e")
        self.greedy_tree.column("value", width=70, anchor="center")

        scroll2 = ttk.Scrollbar(tree2_frame, orient="vertical", command=self.greedy_tree.yview)
        self.greedy_tree.configure(yscrollcommand=scroll2.set)
        self.greedy_tree.pack(side="left", fill="both", expand=True)
        scroll2.pack(side="right", fill="y")

        # Bottom Viva Explanation Card
        exp_box = ctk.CTkFrame(self, fg_color="#181A26", corner_radius=10)
        exp_box.pack(fill="x", padx=20, pady=(5, 12))

        self.explanation_lbl = ctk.CTkLabel(
            exp_box,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#CBD5E1",
            justify="left"
        )
        self.explanation_lbl.pack(anchor="w", padx=15, pady=8)

    def _set_budget(self, val):
        self.current_budget = val
        self.budget_entry.delete(0, "end")
        self.budget_entry.insert(0, str(val))
        self.optimize()

    def optimize(self):
        try:
            self.current_budget = max(0, int(float(self.budget_entry.get().strip())))
        except ValueError:
            self.current_budget = 5000

        products = self.get_products()
        if not products:
            return

        # 1. Run 0/1 Knapsack (DP)
        dp_res = solve_01_knapsack(products, self.current_budget)
        self.dp_summary_lbl.configure(
            text=f"Total Cost: Rs.{dp_res['total_cost']:,}  |  Total Value: {dp_res['total_value']}  |  "
                 f"Remaining: Rs.{dp_res['remaining_budget']:,}  |  Time: {dp_res['time_ms']} ms"
        )
        for r in self.dp_tree.get_children():
            self.dp_tree.delete(r)
        for p in dp_res["selected_items"]:
            self.dp_tree.insert("", "end", values=(p["product_name"], p["category"], f"Rs.{p['price']:,}", p["priority"]))

        # 2. Run Fractional Knapsack (Greedy)
        gr_res = solve_fractional_knapsack(products, self.current_budget)
        self.greedy_summary_lbl.configure(
            text=f"Total Cost: Rs.{gr_res['total_cost']:,}  |  Total Value: {gr_res['total_value']}  |  "
                 f"Remaining: Rs.{gr_res['remaining_budget']:,}  |  Time: {gr_res['time_ms']} ms"
        )
        for r in self.greedy_tree.get_children():
            self.greedy_tree.delete(r)
        for item in gr_res["selected_items"]:
            q_str = "100%" if item["fraction"] >= 1.0 else f"{round(item['fraction'] * 100, 1)}%"
            self.greedy_tree.insert("", "end", values=(
                item["product_name"], q_str, f"Rs.{round(item['cost'], 1):,}", round(item['value'], 2)
            ))

        # 3. Dynamic Comparison Explanation
        self.explanation_lbl.configure(
            text=f"💡 DAA Comparison:\n"
                 f"• 0/1 Knapsack (DP): Selected {len(dp_res['selected_items'])} whole products achieving {dp_res['total_value']} total priority.\n"
                 f"• Fractional Knapsack (Greedy): Achieved {gr_res['total_value']} total priority by ranking items by value-to-price ratio.\n"
                 f"• Theoretical Guarantee: Fractional Knapsack Value ({gr_res['total_value']}) >= 0/1 Knapsack Value ({dp_res['total_value']}) because fractional selection fills residual budget."
        )
