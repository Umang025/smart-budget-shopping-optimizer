"""
Dashboard Page for Smart Budget and Shopping Optimizer.
Displays key metrics, budget distribution, category charts, and quick actions.
"""

import customtkinter as ctk
import tkinter as tk
from typing import Dict, Any, List, Callable
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms.knapsack import ZeroOneKnapsack


class DashboardPage(ctk.CTkFrame):
    """
    Main Overview Dashboard displaying high-level statistics,
    shopping expenditure, budget utilization, and category analytics.
    """

    def __init__(self, master, get_products: Callable[[], List[Dict[str, Any]]], navigate_to: Callable[[str], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.get_products = get_products
        self.navigate_to = navigate_to
        self.current_budget = 5000

        self.canvas_chart = None
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # Top Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Executive Dashboard & Overview",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#F3F4F6"
        )
        title_label.pack(side="left")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="DAA Project: Dynamic Programming & Greedy Shopping Optimization",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF"
        )
        subtitle_label.pack(side="left", padx=15, pady=(5, 0))

        # Metric Cards Row
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20, pady=10)
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="metric_cards")

        self.card_total_prods = self._create_metric_card(self.cards_frame, 0, "Total Products", "0", "#6C5CE7", "📦")
        self.card_budget = self._create_metric_card(self.cards_frame, 1, "Shopping Budget", "Rs. 0", "#00CEC9", "💳")
        self.card_selected = self._create_metric_card(self.cards_frame, 2, "Selected Items", "0", "#FDCB6E", "🛒")
        self.card_spent = self._create_metric_card(self.cards_frame, 3, "Total Expenditure", "Rs. 0", "#00B894", "💰")
        self.card_remaining = self._create_metric_card(self.cards_frame, 4, "Remaining Balance", "Rs. 0", "#E17055", "⚖️")

        # Quick Budget Setting Panel
        budget_bar = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        budget_bar.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(
            budget_bar,
            text="Quick Budget Control:",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left", padx=(15, 10), pady=12)

        self.budget_entry = ctk.CTkEntry(
            budget_bar,
            placeholder_text="Enter budget (Rs.)",
            width=130,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.budget_entry.insert(0, str(self.current_budget))
        self.budget_entry.pack(side="left", padx=5, pady=12)

        ctk.CTkButton(
            budget_bar,
            text="Apply Budget",
            command=self._on_apply_budget,
            width=110,
            fg_color="#6C5CE7",
            hover_color="#5848C2",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(side="left", padx=8, pady=12)

        # Preset budget pills
        for preset in [1000, 2500, 5000, 10000, 15000]:
            ctk.CTkButton(
                budget_bar,
                text=f"Rs. {preset:,}",
                command=lambda p=preset: self._set_preset_budget(p),
                width=80,
                height=28,
                fg_color="#2B2E42",
                hover_color="#3D405B",
                font=ctk.CTkFont(family="Segoe UI", size=11)
            ).pack(side="left", padx=4, pady=12)

        # Content Split: Left Chart, Right Quick Actions & Insights
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=10)
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left Container: Matplotlib Chart Card
        self.chart_card = ctk.CTkFrame(content_frame, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        self.chart_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        chart_header = ctk.CTkFrame(self.chart_card, fg_color="transparent")
        chart_header.pack(fill="x", padx=15, pady=(12, 5))

        ctk.CTkLabel(
            chart_header,
            text="Catalog Category Distribution & Budget Breakdown",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        self.chart_container = ctk.CTkFrame(self.chart_card, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Right Container: Quick Actions & Educational Viva Highlights
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        ctk.CTkLabel(
            right_panel,
            text="Quick Action Navigation",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        actions = [
            ("⚡ Run Budget Optimizer", "optimizer", "#6C5CE7", "Solve 0/1 Knapsack (DP) & Greedy Knapsack"),
            ("📦 Manage Product Catalog", "product_manager", "#00CEC9", "Add, Edit, Delete and update products.csv"),
            ("🔍 Sort & Binary Search", "search_sort", "#FDCB6E", "Merge Sort & logarithmic price searching"),
            ("📊 Algorithm Complexity & Viva", "algorithm_analysis", "#00B894", "Empirical benchmarks and DAA theory")
        ]

        for title, page_id, color, desc in actions:
            btn_card = ctk.CTkFrame(right_panel, fg_color="#282B40", corner_radius=8)
            btn_card.pack(fill="x", padx=15, pady=6)

            ctk.CTkLabel(
                btn_card,
                text=title,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=color
            ).pack(anchor="w", padx=12, pady=(8, 2))

            ctk.CTkLabel(
                btn_card,
                text=desc,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color="#9CA3AF"
            ).pack(anchor="w", padx=12, pady=(0, 8))

            btn_card.bind("<Button-1>", lambda e, pid=page_id: self.navigate_to(pid))
            for child in btn_card.winfo_children():
                child.bind("<Button-1>", lambda e, pid=page_id: self.navigate_to(pid))

        # Viva Tip Card
        viva_card = ctk.CTkFrame(right_panel, fg_color="#202A36", corner_radius=8, border_width=1, border_color="#00CEC9")
        viva_card.pack(fill="x", padx=15, pady=(15, 15))

        ctk.CTkLabel(
            viva_card,
            text="💡 DAA Viva Quick Concept",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#00CEC9"
        ).pack(anchor="w", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            viva_card,
            text="Dynamic Programming guarantees global optimality for 0/1 Knapsack via Principle of Optimality, whereas Greedy (by V/P ratio) is optimal only when fractional parts are allowed.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#CBD5E1",
            wraplength=280,
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 10))

    def _create_metric_card(self, parent, col, title, value, accent_color, icon):
        card = ctk.CTkFrame(parent, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            top_row,
            text=icon,
            font=ctk.CTkFont(size=18)
        ).pack(side="left")

        ctk.CTkLabel(
            top_row,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#9CA3AF"
        ).pack(side="left", padx=6)

        val_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=accent_color
        )
        val_label.pack(anchor="w", padx=12, pady=(2, 10))

        return val_label

    def _set_preset_budget(self, budget: int):
        self.current_budget = budget
        self.budget_entry.delete(0, "end")
        self.budget_entry.insert(0, str(budget))
        self.refresh()

    def _on_apply_budget(self):
        try:
            val = int(float(self.budget_entry.get().strip()))
            if val < 0:
                val = 0
            self.current_budget = val
            self.refresh()
        except ValueError:
            pass

    def refresh(self):
        """Re-computes dashboard stats and updates charts."""
        products = self.get_products()
        total_products = len(products)

        # Run 0/1 Knapsack to get realistic current spending metrics
        knapsack_res = ZeroOneKnapsack.solve(products, self.current_budget)
        selected_count = len(knapsack_res["selected_products"])
        total_cost = knapsack_res["total_cost"]
        remaining = knapsack_res["remaining_budget"]

        # Update metric labels
        self.card_total_prods.configure(text=f"{total_products}")
        self.card_budget.configure(text=f"Rs. {self.current_budget:,}")
        self.card_selected.configure(text=f"{selected_count} items")
        self.card_spent.configure(text=f"Rs. {total_cost:,}")
        self.card_remaining.configure(text=f"Rs. {remaining:,}")

        # Re-render Matplotlib Chart
        self._render_chart(products, knapsack_res)

    def _render_chart(self, products: List[Dict[str, Any]], knapsack_res: Dict[str, Any]):
        # Clear previous canvas if exists
        for child in self.chart_container.winfo_children():
            child.destroy()

        if not products:
            no_data = ctk.CTkLabel(self.chart_container, text="No products in catalog.", text_color="#9CA3AF")
            no_data.pack(expand=True)
            return

        # Prepare Category Breakdown
        categories: Dict[str, int] = {}
        category_prices: Dict[str, float] = {}
        for p in products:
            cat = p.get("category", "Other")
            categories[cat] = categories.get(cat, 0) + 1
            category_prices[cat] = category_prices.get(cat, 0) + p.get("price", 0)

        # Setup modern dark Matplotlib Figure
        fig = Figure(figsize=(6.2, 3.2), dpi=100, facecolor="#1F2233")
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Donut Chart for Categories
        labels = list(categories.keys())
        sizes = list(categories.values())
        colors = ["#6C5CE7", "#00CEC9", "#FDCB6E", "#E17055", "#00B894", "#E84393"]

        ax1.set_facecolor("#1F2233")
        wedges, texts, autotexts = ax1.pie(
            sizes,
            labels=None,
            autopct="%1.0f%%",
            startangle=140,
            colors=colors[:len(sizes)],
            pctdistance=0.75,
            textprops={"color": "#FFFFFF", "fontsize": 8, "weight": "bold"}
        )
        # Create donut hole
        centre_circle = matplotlib.patches.Circle((0, 0), 0.55, fc="#1F2233")
        ax1.add_patch(centre_circle)
        ax1.set_title("Products by Category", color="#F3F4F6", fontsize=10, weight="bold", pad=8)

        # Add compact legend under pie chart
        ax1.legend(
            wedges,
            [f"{lbl} ({cnt})" for lbl, cnt in zip(labels, sizes)],
            loc="lower center",
            bbox_to_anchor=(0.5, -0.28),
            fontsize=7,
            frameon=False,
            labelcolor="#CBD5E1",
            ncol=2
        )

        # Bar chart for Total Cost by Category
        ax2.set_facecolor("#1F2233")
        short_labels = [c[:8] for c in labels]
        costs = [category_prices[c] for c in labels]
        bars = ax2.bar(short_labels, costs, color=colors[:len(labels)], width=0.55)

        ax2.set_title("Total Value (Rs.) by Category", color="#F3F4F6", fontsize=10, weight="bold", pad=8)
        ax2.tick_params(colors="#9CA3AF", labelsize=7)
        ax2.spines["bottom"].set_color("#2C3048")
        ax2.spines["left"].set_color("#2C3048")
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.yaxis.grid(True, linestyle="--", alpha=0.3, color="#2C3048")

        for bar in bars:
            height = bar.get_height()
            ax2.annotate(
                f"{int(height):,}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 2),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=7, color="#E2E8F0"
            )

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
