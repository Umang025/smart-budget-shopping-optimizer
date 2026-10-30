"""
Product Manager Page (Simplified)
Allows Adding, Deleting, and Viewing Products with automatic CSV persistence.
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable
from utils.csv_handler import load_products, add_product, delete_product, get_next_id


class ProductManagerPage(ctk.CTkFrame):
    CATEGORIES = ["Electronics", "Accessories", "Stationery", "Computer Peripherals", "Daily Essentials"]

    def __init__(self, master, on_data_changed: Callable[[], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_data_changed = on_data_changed

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # Header
        ctk.CTkLabel(
            self,
            text="Product Management",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # Main Layout: Left Table, Right Form
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=5)
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)

        # Left: Table Panel
        left_panel = ctk.CTkFrame(container, fg_color="#1F2233", corner_radius=10)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Search Bar
        search_bar = ctk.CTkFrame(left_panel, fg_color="transparent")
        search_bar.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(search_bar, text="Filter:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(search_bar, placeholder_text="Search name or ID...", width=160)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table())

        ctk.CTkButton(search_bar, text="Delete Selected", fg_color="#EF4444", hover_color="#DC2626", command=self._delete_selected, width=120).pack(side="right", padx=5)

        # Treeview
        tree_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("id", "name", "category", "price", "priority", "divisible")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price (Rs.)")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("divisible", text="Divisible")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=170, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("priority", width=60, anchor="center")
        self.tree.column("divisible", width=70, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Right: Add Product Form
        form_panel = ctk.CTkFrame(container, fg_color="#1F2233", corner_radius=10)
        form_panel.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(form_panel, text="Add New Product", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        self.status_lbl = ctk.CTkLabel(form_panel, text="", font=ctk.CTkFont(size=11), text_color="#10B981")
        self.status_lbl.pack(anchor="w", padx=15, pady=(0, 5))

        f_box = ctk.CTkFrame(form_panel, fg_color="transparent")
        f_box.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(f_box, text="Product ID:").grid(row=0, column=0, sticky="w", pady=6)
        self.id_entry = ctk.CTkEntry(f_box, width=150)
        self.id_entry.grid(row=0, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkLabel(f_box, text="Name:").grid(row=1, column=0, sticky="w", pady=6)
        self.name_entry = ctk.CTkEntry(f_box, width=150)
        self.name_entry.grid(row=1, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkLabel(f_box, text="Category:").grid(row=2, column=0, sticky="w", pady=6)
        self.cat_menu = ctk.CTkOptionMenu(f_box, values=self.CATEGORIES, width=150)
        self.cat_menu.grid(row=2, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkLabel(f_box, text="Price (Rs.):").grid(row=3, column=0, sticky="w", pady=6)
        self.price_entry = ctk.CTkEntry(f_box, width=150)
        self.price_entry.grid(row=3, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkLabel(f_box, text="Priority (1-10):").grid(row=4, column=0, sticky="w", pady=6)
        self.priority_entry = ctk.CTkEntry(f_box, width=150)
        self.priority_entry.grid(row=4, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkLabel(f_box, text="Divisible:").grid(row=5, column=0, sticky="w", pady=6)
        self.div_switch = ctk.CTkSwitch(f_box, text="Allow fractional")
        self.div_switch.grid(row=5, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkButton(form_panel, text="Add Product", fg_color="#10B981", hover_color="#059669", command=self._add_action).pack(fill="x", padx=15, pady=(15, 10))

    def refresh(self):
        self.products = load_products()
        self.filter_table()
        self.id_entry.delete(0, "end")
        self.id_entry.insert(0, get_next_id())

    def filter_table(self):
        q = self.search_entry.get().strip().lower()
        for r in self.tree.get_children():
            self.tree.delete(r)

        for p in self.products:
            if q and (q not in p["product_name"].lower() and q not in p["product_id"].lower()):
                continue
            div_str = "Yes" if p.get("is_divisible") == 1 else "No"
            self.tree.insert("", "end", iid=p["product_id"], values=(
                p["product_id"], p["product_name"], p["category"], f"Rs.{p['price']:,}", p["priority"], div_str
            ))

    def _add_action(self):
        payload = {
            "product_id": self.id_entry.get().strip(),
            "product_name": self.name_entry.get().strip(),
            "category": self.cat_menu.get(),
            "price": self.price_entry.get().strip(),
            "priority": self.priority_entry.get().strip(),
            "is_divisible": self.div_switch.get() == 1
        }
        ok, msg = add_product(payload)
        if ok:
            self.status_lbl.configure(text=msg, text_color="#10B981")
            self.name_entry.delete(0, "end")
            self.price_entry.delete(0, "end")
            self.priority_entry.delete(0, "end")
            self.refresh()
            self.on_data_changed()
        else:
            self.status_lbl.configure(text=msg, text_color="#EF4444")

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Product", "Please select a product from the table to delete.")
            return

        pid = sel[0]
        if messagebox.askyesno("Confirm", f"Delete product {pid}?"):
            ok, msg = delete_product(pid)
            if ok:
                self.status_lbl.configure(text=msg, text_color="#10B981")
                self.refresh()
                self.on_data_changed()
            else:
                self.status_lbl.configure(text=msg, text_color="#EF4444")
