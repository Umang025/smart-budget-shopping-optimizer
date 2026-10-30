"""
Smart Budget and Shopping Optimizer
MCA (Cloud Computing and DevOps) DAA Mini Project
Main Desktop Application Entry Point
"""

import sys
import os

# Set working directory to project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ensure console supports UTF-8 on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import customtkinter as ctk
from typing import Dict, Any, List

from utils.csv_handler import load_products, initialize_csv
from gui.dashboard import DashboardPage
from gui.product_manager import ProductManagerPage
from gui.optimizer import BudgetOptimizerPage
from gui.search_sort import SearchSortPage
from gui.algorithm_analysis import AlgorithmAnalysisPage

# Configure global CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SmartBudgetApp(ctk.CTk):
    """
    Main Application Window for Smart Budget and Shopping Optimizer.
    Manages navigation, page switching, and global state synchronization.
    """

    APP_TITLE = "Smart Budget and Shopping Optimizer | DAA Mini Project"
    WINDOW_WIDTH = 1240
    WINDOW_HEIGHT = 800

    def __init__(self):
        super().__init__()

        # Ensure CSV database is ready
        initialize_csv()
        self.products: List[Dict[str, Any]] = load_products()

        # Window Configuration
        self.title(self.APP_TITLE)
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.minsize(1100, 700)
        self.configure(fg_color="#0F111A")

        # Center window on screen
        self._center_window()

        # Build Main Layout
        self._build_sidebar()
        self._build_content_area()

        # Load initial page
        self.select_page("dashboard")

    def _center_window(self):
        """Centers window on the primary display."""
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = max(0, (screen_w - self.WINDOW_WIDTH) // 2)
        y = max(0, (screen_h - self.WINDOW_HEIGHT) // 2)
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

    def _build_sidebar(self):
        """Constructs the left-hand navigation bar."""
        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#181A26",
            border_width=1,
            border_color="#2C3048"
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        # Brand / App Title Banner
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(24, 20))

        ctk.CTkLabel(
            brand_frame,
            text="🛒 SmartOptimizer",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_frame,
            text="DAA Algorithmic Engine",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#00CEC9"
        ).pack(anchor="w", pady=(2, 0))

        # Horizontal Divider
        divider = ctk.CTkFrame(self.sidebar, height=1, fg_color="#2C3048")
        divider.pack(fill="x", padx=16, pady=(0, 16))

        # Nav Buttons
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        pages = [
            ("dashboard", "📊  Dashboard"),
            ("product_manager", "📦  Product Manager"),
            ("optimizer", "⚡  Budget Optimizer"),
            ("search_sort", "🔍  Sorting & Search"),
            ("algorithm_analysis", "📈  Algorithm Analysis")
        ]

        for page_id, text in pages:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                fg_color="transparent",
                text_color="#CBD5E1",
                hover_color="#23263B",
                corner_radius=8,
                height=42,
                command=lambda pid=page_id: self.select_page(pid)
            )
            btn.pack(fill="x", padx=14, pady=4)
            self.nav_buttons[page_id] = btn

        # Bottom Academic Viva Badge
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="#12131C", corner_radius=10, border_width=1, border_color="#2C3048")
        footer_frame.pack(side="bottom", fill="x", padx=14, pady=20)

        ctk.CTkLabel(
            footer_frame,
            text="🎓 MCA Mini Project",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#A29BFE"
        ).pack(anchor="w", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            footer_frame,
            text="Design & Analysis of Algorithms\n• 0/1 Knapsack (DP)\n• Fractional Knapsack (Greedy)\n• Merge Sort (D&C)\n• Binary Search (D&C)",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color="#9CA3AF",
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 8))

    def _build_content_area(self):
        """Constructs container for rendering the active page."""
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True)

        # Initialize all 5 pages
        self.pages: Dict[str, ctk.CTkFrame] = {}

        self.pages["dashboard"] = DashboardPage(
            self.content_container,
            get_products=self.get_latest_products,
            navigate_to=self.select_page
        )
        self.pages["product_manager"] = ProductManagerPage(
            self.content_container,
            on_data_changed=self.on_data_updated
        )
        self.pages["optimizer"] = BudgetOptimizerPage(
            self.content_container,
            get_products=self.get_latest_products
        )
        self.pages["search_sort"] = SearchSortPage(
            self.content_container,
            get_products=self.get_latest_products
        )
        self.pages["algorithm_analysis"] = AlgorithmAnalysisPage(
            self.content_container
        )

    def get_latest_products(self) -> List[Dict[str, Any]]:
        """Returns the in-memory or loaded product list."""
        return self.products

    def on_data_updated(self):
        """Called whenever products are added, edited, or deleted in Product Manager."""
        self.products = load_products()
        # Refresh dashboard
        if "dashboard" in self.pages:
            self.pages["dashboard"].refresh()
        # Refresh optimizer if instantiated
        if "optimizer" in self.pages:
            self.pages["optimizer"].run_optimization()
        # Refresh search & sort
        if "search_sort" in self.pages:
            self.pages["search_sort"].run_merge_sort()

    def select_page(self, page_id: str):
        """Switches the visible page and highlights sidebar selection."""
        # Update sidebar button states
        for pid, btn in self.nav_buttons.items():
            if pid == page_id:
                btn.configure(fg_color="#6C5CE7", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color="#CBD5E1")

        # Hide all pages and show target page
        for pid, page in self.pages.items():
            if pid == page_id:
                page.pack(fill="both", expand=True)
                # Auto-refresh page on entry if available
                if hasattr(page, "refresh"):
                    page.refresh()
            else:
                page.pack_forget()


def main():
    try:
        app = SmartBudgetApp()
        app.mainloop()
    except Exception as e:
        print(f"Fatal Application Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
