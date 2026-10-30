"""
CSV Handler Utility for Smart Budget and Shopping Optimizer.
Handles direct reading, writing, updating, and initialization of products.csv
without external database dependencies.
"""

import csv
import os
from typing import List, Dict, Any, Optional

DEFAULT_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "products.csv")

# 18 curated sample products across 5 categories
INITIAL_PRODUCTS = [
    {"product_id": "P101", "product_name": "Noise-Cancelling Headphones", "category": "Electronics", "price": 3500, "priority": 9, "is_divisible": 0},
    {"product_id": "P102", "product_name": "Smart Fitness Watch", "category": "Electronics", "price": 2200, "priority": 7, "is_divisible": 0},
    {"product_id": "P103", "product_name": "10000mAh Power Bank", "category": "Electronics", "price": 1100, "priority": 6, "is_divisible": 0},
    {"product_id": "P104", "product_name": "Portable Bluetooth Speaker", "category": "Electronics", "price": 1500, "priority": 5, "is_divisible": 0},
    {"product_id": "P105", "product_name": "Water-Resistant Backpack", "category": "Accessories", "price": 1400, "priority": 8, "is_divisible": 0},
    {"product_id": "P106", "product_name": "Insulated Steel Bottle", "category": "Accessories", "price": 450, "priority": 6, "is_divisible": 0},
    {"product_id": "P107", "product_name": "Polarized UV Sunglasses", "category": "Accessories", "price": 850, "priority": 4, "is_divisible": 0},
    {"product_id": "P108", "product_name": "Memory Foam Neck Pillow", "category": "Accessories", "price": 650, "priority": 5, "is_divisible": 0},
    {"product_id": "P109", "product_name": "Hardcover Dotted Journal", "category": "Stationery", "price": 350, "priority": 7, "is_divisible": 0},
    {"product_id": "P110", "product_name": "Premium Metal Pen Set", "category": "Stationery", "price": 500, "priority": 5, "is_divisible": 0},
    {"product_id": "P111", "product_name": "Multi-tier Desk Organizer", "category": "Stationery", "price": 750, "priority": 6, "is_divisible": 0},
    {"product_id": "P112", "product_name": "Sticky Notes & Tab Pack", "category": "Stationery", "price": 200, "priority": 4, "is_divisible": 0},
    {"product_id": "P113", "product_name": "Mechanical Gaming Keyboard", "category": "Computer Peripherals", "price": 2800, "priority": 9, "is_divisible": 0},
    {"product_id": "P114", "product_name": "Wireless Ergonomic Mouse", "category": "Computer Peripherals", "price": 950, "priority": 7, "is_divisible": 0},
    {"product_id": "P115", "product_name": "1080p Streaming Webcam", "category": "Computer Peripherals", "price": 1800, "priority": 8, "is_divisible": 0},
    {"product_id": "P116", "product_name": "Extended Desk Mousepad", "category": "Computer Peripherals", "price": 400, "priority": 5, "is_divisible": 0},
    {"product_id": "P117", "product_name": "Roasted Coffee Beans (1kg)", "category": "Daily Essentials", "price": 800, "priority": 8, "is_divisible": 1},
    {"product_id": "P118", "product_name": "California Almonds (1kg)", "category": "Daily Essentials", "price": 900, "priority": 7, "is_divisible": 1},
    {"product_id": "P119", "product_name": "Gourmet Dark Chocolate Bites", "category": "Daily Essentials", "price": 300, "priority": 6, "is_divisible": 1},
    {"product_id": "P120", "product_name": "Organic Green Tea (500g)", "category": "Daily Essentials", "price": 450, "priority": 7, "is_divisible": 1},
]

CSV_HEADERS = ["product_id", "product_name", "category", "price", "priority", "is_divisible"]


def initialize_csv(filepath: str = DEFAULT_CSV_PATH) -> None:
    """Create the products.csv file with default sample products if it doesn't exist."""
    if not os.path.exists(filepath):
        save_all_products(INITIAL_PRODUCTS, filepath)


def load_products(filepath: str = DEFAULT_CSV_PATH) -> List[Dict[str, Any]]:
    """
    Read products directly from the CSV file.
    Automatically handles 5-column or 6-column formats for backward compatibility.
    """
    if not os.path.exists(filepath):
        initialize_csv(filepath)

    products = []
    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row or not row.get("product_id"):
                    continue
                try:
                    product = {
                        "product_id": str(row.get("product_id", "")).strip(),
                        "product_name": str(row.get("product_name", "")).strip(),
                        "category": str(row.get("category", "General")).strip(),
                        "price": int(float(row.get("price", 0))),
                        "priority": int(float(row.get("priority", 1))),
                        "is_divisible": int(float(row.get("is_divisible", 1 if row.get("category") == "Daily Essentials" else 0)))
                    }
                    products.append(product)
                except (ValueError, TypeError):
                    continue
    except Exception as e:
        print(f"Error reading CSV file at {filepath}: {e}")
        return []

    return products


def save_all_products(products: List[Dict[str, Any]], filepath: str = DEFAULT_CSV_PATH) -> bool:
    """Write the full product list directly to the CSV file."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for prod in products:
                writer.writerow({
                    "product_id": prod.get("product_id", ""),
                    "product_name": prod.get("product_name", ""),
                    "category": prod.get("category", "General"),
                    "price": int(prod.get("price", 0)),
                    "priority": int(prod.get("priority", 1)),
                    "is_divisible": int(prod.get("is_divisible", 0))
                })
        return True
    except Exception as e:
        print(f"Error saving CSV file at {filepath}: {e}")
        return False


def add_product(product: Dict[str, Any], filepath: str = DEFAULT_CSV_PATH) -> tuple[bool, str]:
    """Validate and add a new product to the CSV file."""
    # Validation
    prod_id = str(product.get("product_id", "")).strip()
    prod_name = str(product.get("product_name", "")).strip()
    category = str(product.get("category", "")).strip()

    if not prod_id:
        return False, "Product ID cannot be empty."
    if not prod_name:
        return False, "Product name cannot be empty."
    if not category:
        return False, "Category cannot be empty."

    try:
        price = int(float(product.get("price", 0)))
        if price <= 0:
            return False, "Price must be a positive number greater than 0."
    except (ValueError, TypeError):
        return False, "Invalid price value."

    try:
        priority = int(float(product.get("priority", 1)))
        if priority < 1 or priority > 100:
            return False, "Priority must be an integer between 1 and 100."
    except (ValueError, TypeError):
        return False, "Invalid priority value."

    is_divisible = 1 if product.get("is_divisible") in (1, "1", True, "True", "true") else 0

    products = load_products(filepath)
    # Check duplicate ID
    for existing in products:
        if existing["product_id"].upper() == prod_id.upper():
            return False, f"Product ID '{prod_id}' already exists. Please use a unique ID."

    new_prod = {
        "product_id": prod_id,
        "product_name": prod_name,
        "category": category,
        "price": price,
        "priority": priority,
        "is_divisible": is_divisible
    }
    products.append(new_prod)
    if save_all_products(products, filepath):
        return True, "Product added successfully."
    return False, "Failed to write product to CSV."


def update_product(product_id: str, updated_data: Dict[str, Any], filepath: str = DEFAULT_CSV_PATH) -> tuple[bool, str]:
    """Update an existing product by product_id."""
    products = load_products(filepath)
    target_idx = None
    for idx, prod in enumerate(products):
        if prod["product_id"].upper() == product_id.upper():
            target_idx = idx
            break

    if target_idx is None:
        return False, f"Product with ID '{product_id}' not found."

    # Validate updated fields
    try:
        price = int(float(updated_data.get("price", products[target_idx]["price"])))
        if price <= 0:
            return False, "Price must be greater than 0."
    except (ValueError, TypeError):
        return False, "Invalid price."

    try:
        priority = int(float(updated_data.get("priority", products[target_idx]["priority"])))
        if priority < 1 or priority > 100:
            return False, "Priority must be between 1 and 100."
    except (ValueError, TypeError):
        return False, "Invalid priority."

    prod_name = str(updated_data.get("product_name", products[target_idx]["product_name"])).strip()
    if not prod_name:
        return False, "Product name cannot be empty."

    category = str(updated_data.get("category", products[target_idx]["category"])).strip()
    if not category:
        return False, "Category cannot be empty."

    is_divisible = 1 if updated_data.get("is_divisible") in (1, "1", True, "True", "true") else 0

    products[target_idx]["product_name"] = prod_name
    products[target_idx]["category"] = category
    products[target_idx]["price"] = price
    products[target_idx]["priority"] = priority
    products[target_idx]["is_divisible"] = is_divisible

    if save_all_products(products, filepath):
        return True, "Product updated successfully."
    return False, "Failed to update product in CSV."


def delete_product(product_id: str, filepath: str = DEFAULT_CSV_PATH) -> tuple[bool, str]:
    """Delete a product by product_id."""
    products = load_products(filepath)
    new_list = [p for p in products if p["product_id"].upper() != product_id.upper()]

    if len(new_list) == len(products):
        return False, f"Product with ID '{product_id}' not found."

    if save_all_products(new_list, filepath):
        return True, "Product deleted successfully."
    return False, "Failed to remove product from CSV."


def generate_next_id(filepath: str = DEFAULT_CSV_PATH) -> str:
    """Generate the next sequential Product ID like P121."""
    products = load_products(filepath)
    max_num = 100
    for p in products:
        pid = p["product_id"].upper()
        if pid.startswith("P") and pid[1:].isdigit():
            max_num = max(max_num, int(pid[1:]))
    return f"P{max_num + 1}"
