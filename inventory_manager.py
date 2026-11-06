import json
import os
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

FILENAME = "inventory.json"


def create_product(item):
    product_type = item.get("type")
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"])
    elif product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"])
    return None


def load_inventory(inventory):
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data:
            product = create_product(item)
            if product is not None:
                inventory.add_product(product)
            else:
                print(f"Skipping item with unknown type: {item.get('id')}")
        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("No inventory.json found. Starting with empty inventory.")


def save_inventory(inventory):
    data = [product.to_dict() for product in inventory.get_products()]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")


def add_product(inventory):
    print("Add New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Select product type: ")
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    if type_choice == "1":
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = float(input("Download Size (MB): "))
        product = DigitalProduct(product_id, name, price, stock, download_size)

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory):
    print("Update Stock")
    search_id = input("Enter Product ID: ")
    product = inventory.search_product(search_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_stock = int(input("New Stock Quantity: "))
    if product.update_stock(new_stock):
        print("Stock updated successfully!")
    else:
        print("Invalid stock quantity. Stock cannot be negative.")


def search_product(inventory):
    print("Search Product")
    search_id = input("Enter Product ID: ")
    product = inventory.search_product(search_id)
    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        print("--------------------")
        product.display_information()
        print("--------------------")


def menu(inventory):
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


inventory = Inventory()
load_inventory(inventory)
menu(inventory)