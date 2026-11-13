import json
import os
from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from inventory import Inventory
from input_helpers import get_positive_float, get_int, get_non_negative_int

FILENAME = "inventory.json"

# Suppliers are independent objects. Products only hold a reference to one (association).
suppliers: dict[str, Supplier] = {}

# Menu choice -> (product type for the factory, prompt for the type-specific value)
PRODUCT_CHOICES: dict[str, tuple[str, str]] = {
    "1": ("physical", "Weight (kg): "),
    "2": ("digital", "Download Size (MB): "),
}


def get_or_create_supplier(supplier_id: str, name: str, contact_email: str) -> Supplier:
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, name, contact_email)
    return suppliers[supplier_id]


def create_product(item: dict) -> Product:
    supplier_data = item["supplier"]
    supplier = get_or_create_supplier(supplier_data["id"], supplier_data["name"],
                                      supplier_data["contact_email"])
    product_type = item["type"]
    extra_key = "weight" if product_type == "physical" else "download_size"
    return ProductFactory.create(product_type, item["id"], item["name"], item["price"],
                                 item["stock"], supplier, item.get(extra_key, 0.0))


def load_inventory(inventory: Inventory) -> None:
    if not os.path.exists(FILENAME):
        print("No inventory.json found. Starting with empty inventory.")
        return
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("inventory.json is not valid JSON. Starting with empty inventory.")
        return
    for item in data:
        try:
            product = create_product(item)
        except (KeyError, ValueError) as error:
            print(f"Skipping item {item.get('id')}: bad or missing data ({error})")
        else:
            inventory.add_product(product)
    print("inventory.json found.")
    print("Inventory loaded successfully.")


def save_inventory(inventory: Inventory) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")


def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Select product type: ")
    if type_choice not in PRODUCT_CHOICES:
        print("Invalid product type.")
        return
    product_type, extra_prompt = PRODUCT_CHOICES[type_choice]

    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    supplier_id = input("Supplier ID: ")
    if supplier_id in suppliers:
        supplier = suppliers[supplier_id]
        print(f"Using existing supplier: {supplier.get_name()}")
    else:
        supplier_name = input("Supplier Name: ")
        supplier_email = input("Supplier Email: ")
        supplier = get_or_create_supplier(supplier_id, supplier_name, supplier_email)

    extra_value = get_positive_float(extra_prompt)

    try:
        product = ProductFactory.create(product_type, product_id, name, price,
                                        stock, supplier, extra_value)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")
    search_id = input("Enter Product ID: ")
    product = inventory.find_product(search_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_stock = get_int("New Stock Quantity: ")
    if product.update_stock(new_stock):
        print("Stock updated successfully!")
    else:
        print("Invalid stock quantity. Stock cannot be negative.")


def search_product(inventory: Inventory) -> None:
    print("Search Product")
    search_id = input("Enter Product ID: ")
    product = inventory.find_product(search_id)
    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        print("--------------------")
        product.display_information()
        product.get_supplier().display_information()
        print("--------------------")


def menu(inventory: Inventory) -> None:
    while True:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        choice = input("Enter option: ")

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    inventory = Inventory()
    load_inventory(inventory)
    menu(inventory)