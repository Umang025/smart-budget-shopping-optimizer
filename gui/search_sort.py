"""
Sorting & Searching Page (Simplified)
Implements Merge Sort (Divide & Conquer) and Binary Search (Decrease & Conquer).
"""

import customtkinter as ctk
from tkinter import ttk
from typing import Dict, Any, List, Callable
from algorithms.merge_sort import merge_sort
from algorithms.binary_search import binary_search_exact


class SearchSortPage(ctk.CTkFrame):
    def __init__(self, master, get_products: Callable[[], List[Dict[str, Any]]], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.get_products = get_products

        self._build_ui()
        self.sort_products()

    def _build_ui(self):
        # Header
        ctk.CTkLabel(
            self,
            text="Sorting & Searching (Merge Sort & Binary Search)",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # Main Split Frame
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=5)
        container.grid_columnconfigure((0, 1), weight=1)
        container.grid_rowconfigure(0, weight=1)

        # -----------------------------
        # LEFT: MERGE SORT
        # -----------------------------
        left_box = ctk.CTkFrame(container, fg_color="#1F2233", corner_radius=10)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        ctk.CTkLabel(left_box, text="Merge Sort (Divide & Conquer)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#A29BFE").pack(anchor="w", padx=12, pady=(10, 4))

        # Sort Controls
        sort_bar = ctk.CTkFrame(left_box, fg_color="transparent")
        sort_bar.pack(fill="x", padx=10, pady=4)

        ctk.CTkLabel(sort_bar, text="Sort By:").pack(side="left", padx=2)
        self.sort_key = ctk.CTkOptionMenu(sort_bar, values=["Price", "Priority", "Product Name"], width=105)
        self.sort_key.set("Price")
        self.sort_key.pack(side="left", padx=4)

        self.sort_order = ctk.CTkOptionMenu(sort_bar, values=["Ascending", "Descending"], width=110)
        self.sort_order.set("Ascending")
        self.sort_order.pack(side="left", padx=4)

        ctk.CTkButton(sort_bar, text="Sort", command=self.sort_products, width=70, fg_color="#6C5CE7").pack(side="left", padx=6)

        self.sort_stats = ctk.CTkLabel(left_box, text="", font=ctk.CTkFont(size=11), text_color="#00CEC9")
        self.sort_stats.pack(anchor="w", padx=12, pady=2)

        # Sorted Table
        tree1_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        tree1_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols1 = ("id", "name", "price", "priority")
        self.sort_tree = ttk.Treeview(tree1_frame, columns=cols1, show="headings", height=12)
        self.sort_tree.heading("id", text="ID")
        self.sort_tree.heading("name", text="Product Name")
        self.sort_tree.heading("price", text="Price (Rs.)")
        self.sort_tree.heading("priority", text="Priority")
        self.sort_tree.column("id", width=50, anchor="center")
        self.sort_tree.column("name", width=160)
        self.sort_tree.column("price", width=75, anchor="e")
        self.sort_tree.column("priority", width=60, anchor="center")

        scroll1 = ttk.Scrollbar(tree1_frame, orient="vertical", command=self.sort_tree.yview)
        self.sort_tree.configure(yscrollcommand=scroll1.set)
        self.sort_tree.pack(side="left", fill="both", expand=True)
        scroll1.pack(side="right", fill="y")

        # -----------------------------
        # RIGHT: BINARY SEARCH
        # -----------------------------
        right_box = ctk.CTkFrame(container, fg_color="#1F2233", corner_radius=10)
        right_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        ctk.CTkLabel(right_box, text="Binary Search (Decrease & Conquer)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00CEC9").pack(anchor="w", padx=12, pady=(10, 4))

        # Search Controls
        search_bar = ctk.CTkFrame(right_box, fg_color="transparent")
        search_bar.pack(fill="x", padx=10, pady=4)

        ctk.CTkLabel(search_bar, text="Search Price (Rs.):").pack(side="left", padx=2)
        self.search_entry = ctk.CTkEntry(search_bar, width=100)
        self.search_entry.insert(0, "450")
        self.search_entry.pack(side="left", padx=4)

        ctk.CTkButton(search_bar, text="Search", command=self.search_product, width=80, fg_color="#00CEC9", text_color="#000000").pack(side="left", padx=6)

        self.search_stats = ctk.CTkLabel(right_box, text="", font=ctk.CTkFont(size=11), text_color="#FDCB6E")
        self.search_stats.pack(anchor="w", padx=12, pady=2)

        # Search Matches Table
        tree2_frame = ctk.CTkFrame(right_box, fg_color="transparent")
        tree2_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.search_tree = ttk.Treeview(tree2_frame, columns=cols1, show="headings", height=5)
        for c in cols1:
            self.search_tree.heading(c, text=c.capitalize())
        self.search_tree.heading("price", text="Price (Rs.)")
        self.search_tree.column("id", width=50, anchor="center")
        self.search_tree.column("name", width=160)
        self.search_tree.column("price", width=75, anchor="e")
        self.search_tree.column("priority", width=60, anchor="center")

        scroll2 = ttk.Scrollbar(tree2_frame, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scroll2.set)
        self.search_tree.pack(side="left", fill="both", expand=True)
        scroll2.pack(side="right", fill="y")

        # Binary Search Step Trace Log
        ctk.CTkLabel(right_box, text="Binary Search Probe Trace:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=12, pady=(2, 0))
        self.trace_box = ctk.CTkTextbox(right_box, height=75, font=ctk.CTkFont(family="Consolas", size=9))
        self.trace_box.pack(fill="x", padx=10, pady=(2, 10))

    def sort_products(self):
        products = self.get_products()
        if not products:
            return

        key_map = {"Price": "price", "Priority": "priority", "Product Name": "product_name"}
        key = key_map.get(self.sort_key.get(), "price")
        is_asc = self.sort_order.get() == "Ascending"

        sorted_list, comps, time_ms = merge_sort(products, key=key, ascending=is_asc)

        self.sort_stats.configure(text=f"Sorted {len(sorted_list)} items  |  Comparisons: {comps}  |  Time: {time_ms} ms")
        for r in self.sort_tree.get_children():
            self.sort_tree.delete(r)

        for p in sorted_list:
            self.sort_tree.insert("", "end", values=(p["product_id"], p["product_name"], f"Rs.{p['price']:,}", p["priority"]))

    def search_product(self):
        products = self.get_products()
        if not products:
            return

        try:
            target = int(float(self.search_entry.get().strip()))
        except ValueError:
            target = 450

        res = binary_search_exact(products, target)

        self.search_stats.configure(
            text=f"Found: {len(res['matches'])} match(es)  |  Comparisons: {res['comparisons']}  |  Time: {res['time_ms']} ms"
        )

        for r in self.search_tree.get_children():
            self.search_tree.delete(r)
        for p in res["matches"]:
            self.search_tree.insert("", "end", values=(p["product_id"], p["product_name"], f"Rs.{p['price']:,}", p["priority"]))

        self.trace_box.delete("1.0", "end")
        for s in res["steps"]:
            self.trace_box.insert("end", f"Step {s['step']}: [low={s['low']}, mid={s['mid']}, high={s['high']}] -> '{s['mid_name']}' (Rs.{s['mid_price']})\n")
        if not res["matches"]:
            self.trace_box.insert("end", f"Target price Rs.{target} was not found in catalog.\n")
