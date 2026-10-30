"""
Smart Budget and Shopping Optimizer
MCA DAA Mini Project - Main Application
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import customtkinter as ctk
from utils.csv_handler import load_products, init_csv
from gui.dashboard import DashboardPage
from gui.product_manager import ProductManagerPage
from gui.optimizer import BudgetOptimizerPage
from gui.search_sort import SearchSortPage
from gui.algorithm_analysis import AlgorithmAnalysisPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SmartBudgetApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        init_csv()
        self.products = load_products()

        self.title("Smart Budget and Shopping Optimizer | DAA Mini Project")
        self.geometry("1100x720")
        self.minsize(980, 620)
        self.configure(fg_color="#0F111A")

        self._build_sidebar()
        self._build_pages()
        self.select_page("dashboard")

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#181A26")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            self.sidebar,
            text="🛒 Smart Budget\nOptimizer",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F3F4F6",
            justify="left"
        ).pack(anchor="w", padx=18, pady=(20, 15))

        # Nav Buttons
        self.nav_buttons = {}
        pages = [
            ("dashboard", "📊  Dashboard"),
            ("product_manager", "📦  Products"),
            ("optimizer", "⚡  Optimizer"),
            ("search_sort", "🔍  Sort & Search"),
            ("algorithm_analysis", "📈  Analysis")
        ]

        for pid, label in pages:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="transparent",
                text_color="#CBD5E1",
                hover_color="#2B2E42",
                height=38,
                command=lambda p=pid: self.select_page(p)
            )
            btn.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[pid] = btn

        # Footer Viva Info
        footer = ctk.CTkFrame(self.sidebar, fg_color="#12131C", corner_radius=8)
        footer.pack(side="bottom", fill="x", padx=12, pady=15)
        ctk.CTkLabel(
            footer,
            text="🎓 DAA Project\n• 0/1 Knapsack (DP)\n• Fractional (Greedy)\n• Merge Sort (D&C)\n• Binary Search",
            font=ctk.CTkFont(size=10),
            text_color="#9CA3AF",
            justify="left"
        ).pack(padx=10, pady=8, anchor="w")

    def _build_pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="right", fill="both", expand=True)

        self.pages = {
            "dashboard": DashboardPage(self.container, self.get_products, self.select_page),
            "product_manager": ProductManagerPage(self.container, self.on_data_updated),
            "optimizer": BudgetOptimizerPage(self.container, self.get_products),
            "search_sort": SearchSortPage(self.container, self.get_products),
            "algorithm_analysis": AlgorithmAnalysisPage(self.container)
        }

    def get_products(self):
        return self.products

    def on_data_updated(self):
        self.products = load_products()
        if "dashboard" in self.pages:
            self.pages["dashboard"].refresh()
        if "optimizer" in self.pages:
            self.pages["optimizer"].optimize()
        if "search_sort" in self.pages:
            self.pages["search_sort"].sort_products()

    def select_page(self, page_id: str):
        for pid, btn in self.nav_buttons.items():
            btn.configure(
                fg_color="#6C5CE7" if pid == page_id else "transparent",
                text_color="#FFFFFF" if pid == page_id else "#CBD5E1"
            )

        for pid, page in self.pages.items():
            if pid == page_id:
                page.pack(fill="both", expand=True)
                if hasattr(page, "refresh"):
                    page.refresh()
            else:
                page.pack_forget()


def main():
    app = SmartBudgetApp()
    app.mainloop()


if __name__ == "__main__":
    main()
