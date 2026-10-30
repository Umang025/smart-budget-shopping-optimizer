"""
Product Management Page for Smart Budget and Shopping Optimizer.
Enables Adding, Editing, Deleting, and Viewing Products with automatic CSV persistence.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable, Optional
from utils.csv_handler import (
    load_products,
    add_product,
    update_product,
    delete_product,
    generate_next_id,
    DEFAULT_CSV_PATH
)


class ProductManagerPage(ctk.CTkFrame):
    """
    CRUD Product Management Interface with validation,
    real-time search filtering, and automatic CSV persistence.
    """

    CATEGORIES = [
        "Electronics",
        "Accessories",
        "Stationery",
        "Computer Peripherals",
        "Daily Essentials"
    ]

    def __init__(self, master, on_data_changed: Callable[[], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_data_changed = on_data_changed
        self.selected_product_id: Optional[str] = None

        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        # Top Header Bar
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Product Catalog Management",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#F3F4F6"
        )
        title_label.pack(side="left")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Direct bidirectional synchronization with products.csv",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF"
        )
        subtitle.pack(side="left", padx=15, pady=(5, 0))

        # Action / Filter Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="#1F2233", corner_radius=10, border_width=1, border_color="#2C3048")
        toolbar.pack(fill="x", padx=25, pady=(5, 12))

        ctk.CTkLabel(
            toolbar,
            text="Search:",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#E2E8F0"
        ).pack(side="left", padx=(15, 6), pady=10)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Filter by name or ID...",
            width=200,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.search_entry.pack(side="left", padx=5, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table())

        ctk.CTkLabel(
            toolbar,
            text="Category:",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#E2E8F0"
        ).pack(side="left", padx=(15, 6), pady=10)

        self.category_filter = ctk.CTkOptionMenu(
            toolbar,
            values=["All Categories"] + self.CATEGORIES,
            command=lambda _: self.filter_table(),
            width=160,
            fg_color="#2B2E42",
            button_color="#3D405B"
        )
        self.category_filter.set("All Categories")
        self.category_filter.pack(side="left", padx=5, pady=10)

        # Right Toolbar Buttons
        ctk.CTkButton(
            toolbar,
            text="+ Add New Product",
            command=self.prepare_new_product_form,
            fg_color="#6C5CE7",
            hover_color="#5848C2",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            width=140
        ).pack(side="right", padx=15, pady=10)

        ctk.CTkButton(
            toolbar,
            text="🔄 Refresh",
            command=self.refresh_table,
            fg_color="#2B2E42",
            hover_color="#3D405B",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            width=90
        ).pack(side="right", padx=5, pady=10)

        # Main Workspace: Left Table (Treeview), Right Form
        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        workspace.grid_columnconfigure(0, weight=3)
        workspace.grid_columnconfigure(1, weight=2)
        workspace.grid_rowconfigure(0, weight=1)

        # Left Table Frame
        table_container = ctk.CTkFrame(workspace, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        table_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        table_header = ctk.CTkFrame(table_container, fg_color="transparent")
        table_header.pack(fill="x", padx=15, pady=(12, 6))

        self.table_count_label = ctk.CTkLabel(
            table_header,
            text="Products in Database: 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#9CA3AF"
        )
        self.table_count_label.pack(side="left")

        # Custom ttk Treeview Styling for Modern Dark Theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "ProductTree.Treeview",
            background="#181A26",
            foreground="#F3F4F6",
            fieldbackground="#181A26",
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=28
        )
        self.style.configure(
            "ProductTree.Treeview.Heading",
            background="#25273C",
            foreground="#00CEC9",
            borderwidth=0,
            font=("Segoe UI", 10, "bold")
        )
        self.style.map(
            "ProductTree.Treeview",
            background=[("selected", "#6C5CE7")],
            foreground=[("selected", "#FFFFFF")]
        )

        tree_scroll_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        tree_scroll_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        columns = ("id", "name", "category", "price", "priority", "divisible")
        self.tree = ttk.Treeview(
            tree_scroll_frame,
            columns=columns,
            show="headings",
            style="ProductTree.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price (Rs.)")
        self.tree.heading("priority", text="Priority (1-10)")
        self.tree.heading("divisible", text="Divisible")

        self.tree.column("id", width=65, anchor="center")
        self.tree.column("name", width=190, anchor="w")
        self.tree.column("category", width=130, anchor="w")
        self.tree.column("price", width=85, anchor="e")
        self.tree.column("priority", width=95, anchor="center")
        self.tree.column("divisible", width=75, anchor="center")

        tree_y_scroll = ttk.Scrollbar(tree_scroll_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_y_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_y_scroll.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Right Side: Form Card
        self.form_card = ctk.CTkFrame(workspace, fg_color="#1F2233", corner_radius=12, border_width=1, border_color="#2C3048")
        self.form_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.form_title = ctk.CTkLabel(
            self.form_card,
            text="Product Details Editor",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#F3F4F6"
        )
        self.form_title.pack(anchor="w", padx=20, pady=(16, 12))

        # Status Message Label
        self.status_label = ctk.CTkLabel(
            self.form_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#10B981"
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 6))

        # Form Fields
        fields_container = ctk.CTkFrame(self.form_card, fg_color="transparent")
        fields_container.pack(fill="x", padx=20, pady=5)

        # Product ID
        ctk.CTkLabel(fields_container, text="Product ID:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=0, column=0, sticky="w", pady=6)
        self.id_entry = ctk.CTkEntry(fields_container, placeholder_text="e.g. P121", font=ctk.CTkFont(size=12))
        self.id_entry.grid(row=0, column=1, sticky="ew", pady=6, padx=(10, 0))

        # Product Name
        ctk.CTkLabel(fields_container, text="Product Name:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=1, column=0, sticky="w", pady=6)
        self.name_entry = ctk.CTkEntry(fields_container, placeholder_text="e.g. Wireless Mouse", font=ctk.CTkFont(size=12))
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=6, padx=(10, 0))

        # Category
        ctk.CTkLabel(fields_container, text="Category:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=2, column=0, sticky="w", pady=6)
        self.category_combo = ctk.CTkComboBox(fields_container, values=self.CATEGORIES, font=ctk.CTkFont(size=12))
        self.category_combo.grid(row=2, column=1, sticky="ew", pady=6, padx=(10, 0))

        # Price
        ctk.CTkLabel(fields_container, text="Price (Rs.):", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=3, column=0, sticky="w", pady=6)
        self.price_entry = ctk.CTkEntry(fields_container, placeholder_text="e.g. 1500", font=ctk.CTkFont(size=12))
        self.price_entry.grid(row=3, column=1, sticky="ew", pady=6, padx=(10, 0))

        # Priority / Value
        ctk.CTkLabel(fields_container, text="Priority (1-10):", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=4, column=0, sticky="w", pady=6)
        self.priority_entry = ctk.CTkEntry(fields_container, placeholder_text="1 to 10", font=ctk.CTkFont(size=12))
        self.priority_entry.grid(row=4, column=1, sticky="ew", pady=6, padx=(10, 0))

        # Divisible switch
        ctk.CTkLabel(fields_container, text="Divisible Item:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CBD5E1").grid(row=5, column=0, sticky="w", pady=6)
        self.divisible_switch = ctk.CTkSwitch(
            fields_container,
            text="Allow fractional buying (e.g. groceries)",
            progress_color="#00CEC9",
            font=ctk.CTkFont(size=11)
        )
        self.divisible_switch.grid(row=5, column=1, sticky="w", pady=6, padx=(10, 0))

        fields_container.grid_columnconfigure(1, weight=1)

        # Form Buttons
        btn_box = ctk.CTkFrame(self.form_card, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(20, 10))

        self.save_btn = ctk.CTkButton(
            btn_box,
            text="💾 Save Product",
            command=self.save_product_action,
            fg_color="#10B981",
            hover_color="#059669",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.save_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.delete_btn = ctk.CTkButton(
            btn_box,
            text="🗑️ Delete",
            command=self.delete_product_action,
            fg_color="#EF4444",
            hover_color="#DC2626",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.delete_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

        ctk.CTkButton(
            self.form_card,
            text="Clear / New",
            command=self.prepare_new_product_form,
            fg_color="#2B2E42",
            hover_color="#3D405B",
            font=ctk.CTkFont(size=12)
        ).pack(fill="x", padx=20, pady=(0, 15))

        # Informational Note
        note_box = ctk.CTkFrame(self.form_card, fg_color="#181A26", corner_radius=8)
        note_box.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(
            note_box,
            text="📌 DAA Knapsack Note:\n- Priority represents value (benefit).\n- Price represents weight (cost).\n- Divisible items can be split in Fractional Knapsack.",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF",
            justify="left"
        ).pack(padx=10, pady=8, anchor="w")

    def refresh_table(self):
        """Reload products directly from products.csv and populate the Treeview."""
        self.products = load_products()
        self.filter_table()

    def filter_table(self):
        """Filter table rows based on search text and selected category."""
        query = self.search_entry.get().strip().lower()
        cat_filter = self.category_filter.get()

        # Clear existing items in Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        matched_count = 0
        for p in self.products:
            # Check category match
            if cat_filter != "All Categories" and p.get("category") != cat_filter:
                continue

            # Check query match
            name = p.get("product_name", "").lower()
            pid = p.get("product_id", "").lower()
            if query and (query not in name and query not in pid):
                continue

            div_str = "Yes (kg/part)" if p.get("is_divisible") == 1 else "No (Whole)"
            self.tree.insert(
                "",
                "end",
                iid=p["product_id"],
                values=(
                    p["product_id"],
                    p["product_name"],
                    p["category"],
                    f"Rs. {p['price']:,}",
                    p["priority"],
                    div_str
                )
            )
            matched_count += 1

        self.table_count_label.configure(text=f"Products Displayed: {matched_count} of {len(self.products)}")

    def _on_tree_select(self, event):
        """Triggered when user clicks a row in the Treeview."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        prod_id = selected_items[0]
        self.selected_product_id = prod_id
        target = next((p for p in self.products if p["product_id"] == prod_id), None)
        if not target:
            return

        # Populate form
        self.form_title.configure(text=f"Editing Product [{prod_id}]")
        self.id_entry.delete(0, "end")
        self.id_entry.insert(0, target["product_id"])
        self.id_entry.configure(state="disabled")  # ID cannot be changed in edit mode

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, target["product_name"])

        if target["category"] in self.CATEGORIES:
            self.category_combo.set(target["category"])
        else:
            self.category_combo.set(self.CATEGORIES[0])

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, str(target["price"]))

        self.priority_entry.delete(0, "end")
        self.priority_entry.insert(0, str(target["priority"]))

        if target.get("is_divisible") == 1:
            self.divisible_switch.select()
        else:
            self.divisible_switch.deselect()

        self.status_label.configure(text="Loaded product details.", text_color="#00CEC9")

    def prepare_new_product_form(self):
        """Clears form to add a brand new product with next sequential ID."""
        self.selected_product_id = None
        self.form_title.configure(text="Add New Product")

        next_id = generate_next_id()
        self.id_entry.configure(state="normal")
        self.id_entry.delete(0, "end")
        self.id_entry.insert(0, next_id)

        self.name_entry.delete(0, "end")
        self.category_combo.set(self.CATEGORIES[0])
        self.price_entry.delete(0, "end")
        self.priority_entry.delete(0, "end")
        self.divisible_switch.deselect()

        self.tree.selection_remove(self.tree.selection())
        self.status_label.configure(text="Ready to add new product.", text_color="#9CA3AF")

    def save_product_action(self):
        """Validate input and save either a new or updated product to CSV."""
        prod_id = self.id_entry.get().strip().upper()
        prod_name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        price_raw = self.price_entry.get().strip()
        priority_raw = self.priority_entry.get().strip()
        is_divisible = 1 if self.divisible_switch.get() == 1 else 0

        # Validations
        if not prod_id:
            self.status_label.configure(text="Error: Product ID required.", text_color="#EF4444")
            return
        if not prod_name:
            self.status_label.configure(text="Error: Product Name required.", text_color="#EF4444")
            return
        try:
            price = int(float(price_raw))
            if price <= 0:
                self.status_label.configure(text="Error: Price must be > 0.", text_color="#EF4444")
                return
        except ValueError:
            self.status_label.configure(text="Error: Price must be a valid number.", text_color="#EF4444")
            return

        try:
            priority = int(float(priority_raw))
            if priority < 1 or priority > 100:
                self.status_label.configure(text="Error: Priority must be 1 to 100.", text_color="#EF4444")
                return
        except ValueError:
            self.status_label.configure(text="Error: Priority must be an integer.", text_color="#EF4444")
            return

        payload = {
            "product_id": prod_id,
            "product_name": prod_name,
            "category": category,
            "price": price,
            "priority": priority,
            "is_divisible": is_divisible
        }

        if self.selected_product_id:
            # Updating existing product
            success, msg = update_product(self.selected_product_id, payload)
        else:
            # Adding new product
            success, msg = add_product(payload)

        if success:
            self.status_label.configure(text=msg, text_color="#10B981")
            self.refresh_table()
            self.on_data_changed()
            if not self.selected_product_id:
                self.prepare_new_product_form()
        else:
            self.status_label.configure(text=f"Error: {msg}", text_color="#EF4444")

    def delete_product_action(self):
        """Delete currently selected product with confirmation."""
        if not self.selected_product_id:
            self.status_label.configure(text="Select a product from the table first.", text_color="#F59E0B")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete product '{self.selected_product_id}' from the database?\nThis will update products.csv immediately."
        )
        if not confirm:
            return

        success, msg = delete_product(self.selected_product_id)
        if success:
            self.status_label.configure(text=msg, text_color="#10B981")
            self.refresh_table()
            self.prepare_new_product_form()
            self.on_data_changed()
        else:
            self.status_label.configure(text=f"Error: {msg}", text_color="#EF4444")
