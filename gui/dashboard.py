"""
Dashboard Page (Simplified)
Displays key shopping statistics and a simple Matplotlib chart.
"""

import customtkinter as ctk
from typing import Dict, Any, List, Callable
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms.knapsack import solve_01_knapsack


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, get_products: Callable[[], List[Dict[str, Any]]], navigate_to: Callable[[str], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.get_products = get_products
        self.navigate_to = navigate_to
        self.current_budget = 5000

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # Header
        ctk.CTkLabel(
            self,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # Metric Cards Frame
        cards_box = ctk.CTkFrame(self, fg_color="transparent")
        cards_box.pack(fill="x", padx=15, pady=5)
        cards_box.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_products = self._make_card(cards_box, 0, "Total Products", "0", "#6C5CE7")
        self.lbl_budget = self._make_card(cards_box, 1, "Budget", "Rs. 0", "#00CEC9")
        self.lbl_spent = self._make_card(cards_box, 2, "Optimized Spend", "Rs. 0", "#00B894")
        self.lbl_remaining = self._make_card(cards_box, 3, "Remaining", "Rs. 0", "#FDCB6E")

        # Budget Quick Bar
        budget_bar = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=10)
        budget_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(budget_bar, text="Shopping Budget (Rs.):", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=12, pady=10)

        self.budget_entry = ctk.CTkEntry(budget_bar, width=120)
        self.budget_entry.insert(0, str(self.current_budget))
        self.budget_entry.pack(side="left", padx=5, pady=10)

        ctk.CTkButton(budget_bar, text="Update Budget", command=self._apply_budget, width=110, fg_color="#6C5CE7").pack(side="left", padx=8, pady=10)

        # Quick preset buttons
        for p in [2000, 5000, 10000]:
            ctk.CTkButton(
                budget_bar,
                text=f"Rs.{p:,}",
                command=lambda val=p: self._set_budget(val),
                width=75,
                fg_color="#2B2E42"
            ).pack(side="left", padx=4, pady=10)

        # Chart Container
        self.chart_frame = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=10)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    def _make_card(self, parent, col, title, val, color):
        card = ctk.CTkFrame(parent, fg_color="#1F2233", corner_radius=10)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=11), text_color="#9CA3AF").pack(padx=10, pady=(8, 2))
        lbl = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=18, weight="bold"), text_color=color)
        lbl.pack(padx=10, pady=(0, 8))
        return lbl

    def _set_budget(self, val):
        self.current_budget = val
        self.budget_entry.delete(0, "end")
        self.budget_entry.insert(0, str(val))
        self.refresh()

    def _apply_budget(self):
        try:
            self.current_budget = max(0, int(float(self.budget_entry.get().strip())))
            self.refresh()
        except ValueError:
            pass

    def refresh(self):
        products = self.get_products()
        dp_res = solve_01_knapsack(products, self.current_budget)

        self.lbl_products.configure(text=str(len(products)))
        self.lbl_budget.configure(text=f"Rs.{self.current_budget:,}")
        self.lbl_spent.configure(text=f"Rs.{dp_res['total_cost']:,}")
        self.lbl_remaining.configure(text=f"Rs.{dp_res['remaining_budget']:,}")

        # Draw Simple Matplotlib Bar Chart
        for w in self.chart_frame.winfo_children():
            w.destroy()

        if not products:
            return

        cat_counts = {}
        for p in products:
            c = p.get("category", "Other")
            cat_counts[c] = cat_counts.get(c, 0) + 1

        fig = Figure(figsize=(6, 2.8), dpi=100, facecolor="#1F2233")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#181A26")

        cats = list(cat_counts.keys())
        counts = list(cat_counts.values())
        colors = ["#6C5CE7", "#00CEC9", "#FDCB6E", "#00B894", "#E17055"]

        ax.bar(cats, counts, color=colors[:len(cats)], width=0.5)
        ax.set_title("Products per Category", color="#F3F4F6", fontsize=11, weight="bold")
        ax.tick_params(colors="#CBD5E1", labelsize=8)
        ax.spines["bottom"].set_color("#2C3048")
        ax.spines["left"].set_color("#2C3048")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.3, color="#4A5568")

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
