"""
Sorting and Searching Page for Smart Budget and Shopping Optimizer.
Implements Merge Sort (Divide & Conquer) and Binary Search (Decrease & Conquer)
with real-time performance metrics and execution tracing.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List, Callable
from algorithms.merge_sort import MergeSort
from algorithms.binary_search import BinarySearch


class SearchSortPage(ctk.CTkFrame):
    """
    Workspace for exploring Divide and Conquer (Merge Sort)
    and Decrease and Conquer (Binary Search) with step visualization.
    """

    def __init__(self, master, get_products: Callable[[], List[Dict[str, Any]]], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.get_products = get_products

        self.sorter = MergeSort()
        self.last_sorted_products: List[Dict[str, Any]] = []

        self._build_ui()
        self.run_merge_sort()

    def _build_ui(self):
        # Header Row
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Sorting & Searching Algorithms",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#F3F4F6"
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text="DAA Syllabus: Merge Sort (Divide & Conquer) + Binary Search (Decrease & Conquer)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF"
        ).pack(side="left", padx=15, pady=(5, 0))

        # Main Split Workspace
        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        workspace.grid_columnconfigure((0, 1), weight=1, uniform="search_sort_split")
        workspace.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # LEFT PANEL: MERGE SORT (Divide & Conquer)
        # ----------------------------------------------------
        sort_panel = ctk.CTkFrame(workspace, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        sort_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        sort_header = ctk.CTkFrame(sort_panel, fg_color="transparent")
        sort_header.pack(fill="x", padx=15, pady=(12, 6))

        ctk.CTkLabel(
            sort_header,
            text="🔀 Merge Sort (Divide & Conquer)",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#A29BFE"
        ).pack(side="left")

        ctk.CTkLabel(
            sort_header,
            text="Time: O(n log n) | Space: O(n)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9CA3AF"
        ).pack(side="right")

        # Sort Controls Toolbar
        sort_ctrls = ctk.CTkFrame(sort_panel, fg_color="#181A26", corner_radius=8)
        sort_ctrls.pack(fill="x", padx=12, pady=6)

        ctk.CTkLabel(sort_ctrls, text="Sort By:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.sort_key_menu = ctk.CTkOptionMenu(
            sort_ctrls,
            values=["Price", "Priority", "Product Name", "Product ID"],
            width=120,
            fg_color="#2B2E42",
            button_color="#3D405B"
        )
        self.sort_key_menu.set("Price")
        self.sort_key_menu.grid(row=0, column=1, padx=4, pady=8)

        ctk.CTkLabel(sort_ctrls, text="Order:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.sort_order_menu = ctk.CTkOptionMenu(
            sort_ctrls,
            values=["Ascending (Low to High)", "Descending (High to Low)"],
            width=165,
            fg_color="#2B2E42",
            button_color="#3D405B"
        )
        self.sort_order_menu.set("Ascending (Low to High)")
        self.sort_order_menu.grid(row=0, column=3, padx=4, pady=8)

        ctk.CTkButton(
            sort_ctrls,
            text="Run Merge Sort",
            command=self.run_merge_sort,
            fg_color="#6C5CE7",
            hover_color="#5848C2",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=110
        ).grid(row=0, column=4, padx=8, pady=8)

        # Merge Sort Metrics Banner
        self.sort_metrics_label = ctk.CTkLabel(
            sort_panel,
            text="Comparisons: 0 | Time: 0.0 ms | Elements: 0",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00CEC9"
        )
        self.sort_metrics_label.pack(anchor="w", padx=15, pady=(2, 6))

        # Sorted Items Treeview
        sort_tree_frame = ctk.CTkFrame(sort_panel, fg_color="transparent")
        sort_tree_frame.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        cols = ("id", "name", "category", "price", "priority")
        self.sort_tree = ttk.Treeview(sort_tree_frame, columns=cols, show="headings", style="ProductTree.Treeview", height=8)
        self.sort_tree.heading("id", text="ID")
        self.sort_tree.heading("name", text="Product Name")
        self.sort_tree.heading("category", text="Category")
        self.sort_tree.heading("price", text="Price (Rs.)")
        self.sort_tree.heading("priority", text="Priority")

        self.sort_tree.column("id", width=55, anchor="center")
        self.sort_tree.column("name", width=160, anchor="w")
        self.sort_tree.column("category", width=110, anchor="w")
        self.sort_tree.column("price", width=80, anchor="e")
        self.sort_tree.column("priority", width=65, anchor="center")

        sort_scroll = ttk.Scrollbar(sort_tree_frame, orient="vertical", command=self.sort_tree.yview)
        self.sort_tree.configure(yscrollcommand=sort_scroll.set)
        self.sort_tree.pack(side="left", fill="both", expand=True)
        sort_scroll.pack(side="right", fill="y")

        # Merge Sort Explanation Box
        self.sort_info_box = ctk.CTkLabel(
            sort_panel,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF",
            justify="left",
            wraplength=480
        )
        self.sort_info_box.pack(anchor="w", padx=15, pady=(4, 12))

        # ----------------------------------------------------
        # RIGHT PANEL: BINARY SEARCH (Decrease & Conquer)
        # ----------------------------------------------------
        search_panel = ctk.CTkFrame(workspace, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        search_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        search_header = ctk.CTkFrame(search_panel, fg_color="transparent")
        search_header.pack(fill="x", padx=15, pady=(12, 6))

        ctk.CTkLabel(
            search_header,
            text="🔎 Binary Search (Decrease & Conquer)",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#00CEC9"
        ).pack(side="left")

        ctk.CTkLabel(
            search_header,
            text="Time: O(log n) | Space: O(1)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9CA3AF"
        ).pack(side="right")

        # Search Controls Toolbar
        search_ctrls = ctk.CTkFrame(search_panel, fg_color="#181A26", corner_radius=8)
        search_ctrls.pack(fill="x", padx=12, pady=6)

        ctk.CTkLabel(search_ctrls, text="Mode:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=0, column=0, padx=6, pady=8, sticky="w")
        self.search_mode_menu = ctk.CTkOptionMenu(
            search_ctrls,
            values=["Exact Price Search", "Price Range Search"],
            command=self._on_search_mode_change,
            width=150,
            fg_color="#2B2E42",
            button_color="#3D405B"
        )
        self.search_mode_menu.set("Exact Price Search")
        self.search_mode_menu.grid(row=0, column=1, padx=4, pady=8)

        # Container for dynamic inputs
        self.search_inputs_frame = ctk.CTkFrame(search_ctrls, fg_color="transparent")
        self.search_inputs_frame.grid(row=0, column=2, padx=4, pady=8)
        self._build_exact_search_inputs()

        ctk.CTkButton(
            search_ctrls,
            text="Run Search",
            command=self.run_binary_search,
            fg_color="#00CEC9",
            hover_color="#00B5B0",
            text_color="#0F111A",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100
        ).grid(row=0, column=3, padx=6, pady=8)

        # Search Metrics Banner
        self.search_metrics_label = ctk.CTkLabel(
            search_panel,
            text="Steps: 0 | Comparisons: 0 | Time: 0.0 ms | Matches: 0",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#FDCB6E"
        )
        self.search_metrics_label.pack(anchor="w", padx=15, pady=(2, 6))

        # Search Results Treeview
        search_tree_frame = ctk.CTkFrame(search_panel, fg_color="transparent")
        search_tree_frame.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        self.search_tree = ttk.Treeview(search_tree_frame, columns=cols, show="headings", style="ProductTree.Treeview", height=5)
        for c in cols:
            self.search_tree.heading(c, text=c.capitalize())
        self.search_tree.heading("price", text="Price (Rs.)")

        self.search_tree.column("id", width=55, anchor="center")
        self.search_tree.column("name", width=160, anchor="w")
        self.search_tree.column("category", width=110, anchor="w")
        self.search_tree.column("price", width=80, anchor="e")
        self.search_tree.column("priority", width=65, anchor="center")

        search_scroll = ttk.Scrollbar(search_tree_frame, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=search_scroll.set)
        self.search_tree.pack(side="left", fill="both", expand=True)
        search_scroll.pack(side="right", fill="y")

        # Binary Search Probe Path Textbox
        ctk.CTkLabel(
            search_panel,
            text="Binary Search Probe Intervals (Halving Steps):",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#A29BFE"
        ).pack(anchor="w", padx=15, pady=(4, 2))

        self.search_trace_box = ctk.CTkTextbox(
            search_panel,
            height=70,
            font=ctk.CTkFont(family="Consolas", size=9),
            fg_color="#12131C",
            text_color="#E2E8F0"
        )
        self.search_trace_box.pack(fill="x", padx=12, pady=(0, 8))

        self.search_info_box = ctk.CTkLabel(
            search_panel,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF",
            justify="left",
            wraplength=480
        )
        self.search_info_box.pack(anchor="w", padx=15, pady=(0, 10))

    def _build_exact_search_inputs(self):
        for child in self.search_inputs_frame.winfo_children():
            child.destroy()

        ctk.CTkLabel(self.search_inputs_frame, text="Target Rs:", font=ctk.CTkFont(size=11), text_color="#CBD5E1").pack(side="left", padx=2)
        self.exact_price_entry = ctk.CTkEntry(self.search_inputs_frame, width=80, font=ctk.CTkFont(size=11))
        self.exact_price_entry.insert(0, "450")
        self.exact_price_entry.pack(side="left", padx=2)

    def _build_range_search_inputs(self):
        for child in self.search_inputs_frame.winfo_children():
            child.destroy()

        ctk.CTkLabel(self.search_inputs_frame, text="Min:", font=ctk.CTkFont(size=11), text_color="#CBD5E1").pack(side="left", padx=2)
        self.min_price_entry = ctk.CTkEntry(self.search_inputs_frame, width=65, font=ctk.CTkFont(size=11))
        self.min_price_entry.insert(0, "500")
        self.min_price_entry.pack(side="left", padx=2)

        ctk.CTkLabel(self.search_inputs_frame, text="Max:", font=ctk.CTkFont(size=11), text_color="#CBD5E1").pack(side="left", padx=2)
        self.max_price_entry = ctk.CTkEntry(self.search_inputs_frame, width=65, font=ctk.CTkFont(size=11))
        self.max_price_entry.insert(0, "1500")
        self.max_price_entry.pack(side="left", padx=2)

    def _on_search_mode_change(self, mode: str):
        if mode == "Exact Price Search":
            self._build_exact_search_inputs()
        else:
            self._build_range_search_inputs()

    def run_merge_sort(self):
        """Executes manual Merge Sort with user-selected key and order."""
        products = self.get_products()
        if not products:
            return

        key_map = {
            "Price": "price",
            "Priority": "priority",
            "Product Name": "product_name",
            "Product ID": "product_id"
        }
        chosen_key = key_map.get(self.sort_key_menu.get(), "price")
        is_asc = "Ascending" in self.sort_order_menu.get()

        sorted_prods, comparisons, elapsed_ms, explanation = self.sorter.sort(
            products,
            key=chosen_key,
            ascending=is_asc
        )
        self.last_sorted_products = sorted_prods

        # Populate tree
        for r in self.sort_tree.get_children():
            self.sort_tree.delete(r)

        for p in sorted_prods:
            self.sort_tree.insert(
                "", "end",
                values=(p["product_id"], p["product_name"], p["category"], f"Rs. {p['price']:,}", p["priority"])
            )

        self.sort_metrics_label.configure(
            text=f"Comparisons: {comparisons:,}  |  Time: {elapsed_ms} ms  |  Elements: {len(sorted_prods)}"
        )
        self.sort_info_box.configure(text=explanation)

    def run_binary_search(self):
        """Executes manual Binary Search after ensuring list is sorted by price."""
        products = self.get_products()
        if not products:
            return

        mode = self.search_mode_menu.get()

        for r in self.search_tree.get_children():
            self.search_tree.delete(r)
        self.search_trace_box.delete("1.0", "end")

        if mode == "Exact Price Search":
            try:
                target_val = int(float(self.exact_price_entry.get().strip()))
            except (ValueError, AttributeError):
                target_val = 450

            res = BinarySearch.search_by_exact_price(products, target_val)

            # Trace output
            self.search_trace_box.insert("end", f"Precondition Met: Catalog sorted by Price using Merge Sort.\n")
            for s in res["steps"]:
                self.search_trace_box.insert(
                    "end",
                    f"Step {s['step_num']}: [low={s['low']}, mid={s['mid']}, high={s['high']}] -> "
                    f"'{s['mid_product']}' (Rs.{s['mid_price']}) -> {s['action']}\n"
                )

            self.search_metrics_label.configure(
                text=f"Steps: {len(res['steps'])}  |  Comparisons: {res['comparisons']}  |  "
                     f"Time: {res['execution_time_ms']} ms  |  Matches: {len(res['matching_products'])}"
            )
            self.search_info_box.configure(text=res["explanation"])

            for p in res["matching_products"]:
                self.search_tree.insert(
                    "", "end",
                    values=(p["product_id"], p["product_name"], p["category"], f"Rs. {p['price']:,}", p["priority"])
                )

        else:
            # Range Search
            try:
                min_p = int(float(self.min_price_entry.get().strip()))
                max_p = int(float(self.max_price_entry.get().strip()))
            except (ValueError, AttributeError):
                min_p, max_p = 500, 1500

            res = BinarySearch.search_by_price_range(products, min_p, max_p)

            self.search_trace_box.insert("end", f"Precondition Met: Catalog sorted by Price using Merge Sort.\n")
            self.search_trace_box.insert(
                "end",
                f"Binary Search Lower Bound (Price >= Rs.{min_p}): Index {res['lower_bound_idx']}\n"
                f"Binary Search Upper Bound (Price <= Rs.{max_p}): Index {res['upper_bound_idx']}\n"
                f"Subarray slice [ {res['lower_bound_idx']} : {res['upper_bound_idx']} ] extracted in O(log n + k) time.\n"
            )

            self.search_metrics_label.configure(
                text=f"Comparisons: {res['comparisons']}  |  Time: {res['execution_time_ms']} ms  |  "
                     f"Matches Found: {len(res['matching_products'])}"
            )
            self.search_info_box.configure(text=res["explanation"])

            for p in res["matching_products"]:
                self.search_tree.insert(
                    "", "end",
                    values=(p["product_id"], p["product_name"], p["category"], f"Rs. {p['price']:,}", p["priority"])
                )
