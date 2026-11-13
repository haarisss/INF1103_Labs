import csv
from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row in reader:
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                except ValueError as error:
                    print(f"Skipping row {row}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")