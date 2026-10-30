"""
CSV Handler Utility for Smart Budget and Shopping Optimizer.
Simple, clean data storage in products.csv without external databases.
"""

import csv
import os
from typing import List, Dict, Any, Tuple

CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "products.csv")

SAMPLE_PRODUCTS = [
    {"product_id": "P101", "product_name": "Noise-Cancelling Headphones", "category": "Electronics", "price": 3500, "priority": 9, "is_divisible": 0},
    {"product_id": "P102", "product_name": "Smart Fitness Watch", "category": "Electronics", "price": 2200, "priority": 7, "is_divisible": 0},
    {"product_id": "P103", "product_name": "10000mAh Power Bank", "category": "Electronics", "price": 1100, "priority": 6, "is_divisible": 0},
    {"product_id": "P104", "product_name": "Bluetooth Speaker", "category": "Electronics", "price": 1500, "priority": 5, "is_divisible": 0},
    {"product_id": "P105", "product_name": "Laptop Backpack", "category": "Accessories", "price": 1400, "priority": 8, "is_divisible": 0},
    {"product_id": "P106", "product_name": "Steel Water Bottle", "category": "Accessories", "price": 450, "priority": 6, "is_divisible": 0},
    {"product_id": "P107", "product_name": "Polarized Sunglasses", "category": "Accessories", "price": 850, "priority": 4, "is_divisible": 0},
    {"product_id": "P108", "product_name": "Travel Neck Pillow", "category": "Accessories", "price": 650, "priority": 5, "is_divisible": 0},
    {"product_id": "P109", "product_name": "Dotted Hardcover Journal", "category": "Stationery", "price": 350, "priority": 7, "is_divisible": 0},
    {"product_id": "P110", "product_name": "Metal Ballpoint Pen Set", "category": "Stationery", "price": 500, "priority": 5, "is_divisible": 0},
    {"product_id": "P111", "product_name": "Desk Organizer", "category": "Stationery", "price": 750, "priority": 6, "is_divisible": 0},
    {"product_id": "P112", "product_name": "Sticky Notes Pack", "category": "Stationery", "price": 200, "priority": 4, "is_divisible": 0},
    {"product_id": "P113", "product_name": "Mechanical Keyboard", "category": "Computer Peripherals", "price": 2800, "priority": 9, "is_divisible": 0},
    {"product_id": "P114", "product_name": "Wireless Mouse", "category": "Computer Peripherals", "price": 950, "priority": 7, "is_divisible": 0},
    {"product_id": "P115", "product_name": "1080p HD Webcam", "category": "Computer Peripherals", "price": 1800, "priority": 8, "is_divisible": 0},
    {"product_id": "P116", "product_name": "Extended Mousepad", "category": "Computer Peripherals", "price": 400, "priority": 5, "is_divisible": 0},
    {"product_id": "P117", "product_name": "Coffee Beans (1kg)", "category": "Daily Essentials", "price": 800, "priority": 8, "is_divisible": 1},
    {"product_id": "P118", "product_name": "Almonds Pack (1kg)", "category": "Daily Essentials", "price": 900, "priority": 7, "is_divisible": 1},
    {"product_id": "P119", "product_name": "Dark Chocolate Pack", "category": "Daily Essentials", "price": 300, "priority": 6, "is_divisible": 1},
    {"product_id": "P120", "product_name": "Green Tea Pack", "category": "Daily Essentials", "price": 450, "priority": 7, "is_divisible": 1},
]

CSV_HEADERS = ["product_id", "product_name", "category", "price", "priority", "is_divisible"]


def init_csv():
    """Create products.csv with sample data if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        save_products(SAMPLE_PRODUCTS)


def load_products() -> List[Dict[str, Any]]:
    """Reads all products from CSV file."""
    if not os.path.exists(CSV_FILE):
        init_csv()

    products = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("product_id"):
                    products.append({
                        "product_id": row["product_id"].strip(),
                        "product_name": row["product_name"].strip(),
                        "category": row.get("category", "General").strip(),
                        "price": int(float(row.get("price", 0))),
                        "priority": int(float(row.get("priority", 1))),
                        "is_divisible": int(float(row.get("is_divisible", 0)))
                    })
    except Exception as e:
        print(f"CSV read error: {e}")
    return products


def save_products(products: List[Dict[str, Any]]) -> bool:
    """Writes product list to CSV file."""
    try:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for p in products:
                writer.writerow({
                    "product_id": p["product_id"],
                    "product_name": p["product_name"],
                    "category": p.get("category", "General"),
                    "price": int(p["price"]),
                    "priority": int(p["priority"]),
                    "is_divisible": int(p.get("is_divisible", 0))
                })
        return True
    except Exception as e:
        print(f"CSV write error: {e}")
        return False


def add_product(p: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates and adds a new product to CSV."""
    pid = str(p.get("product_id", "")).strip().upper()
    name = str(p.get("product_name", "")).strip()
    category = str(p.get("category", "")).strip()

    if not pid:
        return False, "Product ID cannot be empty."
    if not name:
        return False, "Product Name cannot be empty."
    if not category:
        return False, "Category cannot be empty."

    try:
        price = int(float(p.get("price", 0)))
        if price <= 0:
            return False, "Price must be a positive number."
    except ValueError:
        return False, "Invalid price."

    try:
        priority = int(float(p.get("priority", 1)))
        if priority < 1 or priority > 10:
            return False, "Priority must be between 1 and 10."
    except ValueError:
        return False, "Invalid priority."

    products = load_products()
    if any(item["product_id"].upper() == pid for item in products):
        return False, f"Product ID '{pid}' already exists!"

    products.append({
        "product_id": pid,
        "product_name": name,
        "category": category,
        "price": price,
        "priority": priority,
        "is_divisible": 1 if p.get("is_divisible") else 0
    })
    save_products(products)
    return True, f"Product '{name}' added successfully."


def delete_product(product_id: str) -> Tuple[bool, str]:
    """Deletes a product by product_id."""
    products = load_products()
    filtered = [p for p in products if p["product_id"].upper() != product_id.upper()]

    if len(filtered) == len(products):
        return False, f"Product '{product_id}' not found."

    save_products(filtered)
    return True, f"Product '{product_id}' deleted."


def get_next_id() -> str:
    """Generates the next ID like P121."""
    products = load_products()
    max_num = 100
    for p in products:
        pid = p["product_id"].upper()
        if pid.startswith("P") and pid[1:].isdigit():
            max_num = max(max_num, int(pid[1:]))
    return f"P{max_num + 1}"
