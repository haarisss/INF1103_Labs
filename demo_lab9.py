from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

# ---------- Section 2: Strategy ----------

print("=== Strategy: order discounts ===")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
lamp = PhysicalProduct("P001", "Desk Lamp", 25.00, 10, supplier, 1.2)
chair = PhysicalProduct("P002", "Office Chair", 150.00, 3, supplier, 8.0)

order = Order("O001")                      # no strategy given -> NoDiscount
order.add_order_line(lamp, 4)              # 100
order.add_order_line(chair, 1)             # 150
print(f"No discount (default):          ${order.calculate_total():.2f}")

order.set_discount(BulkDiscount(200, 20))
print(f"BulkDiscount(200, 20):          ${order.calculate_total():.2f}")

order.set_discount(PercentageDiscount(10))
print(f"set_discount(PercentageDiscount(10)): ${order.calculate_total():.2f}")

order.set_discount(StudentDiscount())
print(f"StudentDiscount (5% off):       ${order.calculate_total():.2f}")

small = Order("O002", BulkDiscount(200, 20))
small.add_order_line(lamp, 1)              # 25, below the threshold
print(f"Small order (25) with Bulk:     ${small.calculate_total():.2f}")


# ---------- Section 3: Factory ----------
from product_factory import ProductFactory

print("\n=== Factory: creating products ===")
item1 = ProductFactory.create("physical", "P010", "Keyboard", 59.90, 20, supplier, 0.9)
item2 = ProductFactory.create("digital", "D010", "Photo Editor", 49.90, 100, supplier, 350)
item1.display_information()
item2.display_information()
print("Return types:", type(item1).__name__, "and", type(item2).__name__)

try:
    ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
except ValueError as error:
    print("Caught ValueError:", error)
    

# ---------- Section 4: Validation ----------
print("\n=== Validation ===")
for label, action in [
    ("Price 0", lambda: ProductFactory.create("physical", "P020", "Free Item", 0, 5, supplier, 1.0)),
    ("Negative stock", lambda: ProductFactory.create("physical", "P021", "Bad Stock", 10.0, -1, supplier, 1.0)),
    ("Order quantity 0", lambda: Order("O003").add_order_line(lamp, 0)),
]:
    try:
        action()
        print(label, "-> accepted (this should not happen)")
    except ValueError as error:
        print(f"{label} -> ValueError: {error}")
        

# ---------- Section 5: Exceptions ----------
from inventory import Inventory
from input_helpers import get_positive_float
from product_loader import load_products

print("\n=== get_positive_float ===")
price = get_positive_float("Enter a price: ")
print("Returned:", price)

print("\n=== load_products: products.csv ===")
csv_inventory = Inventory()
load_products("products.csv", csv_inventory, supplier)
csv_inventory.display_all()

print("\n=== load_products: file that does not exist ===")
load_products("missing_products.csv", csv_inventory, supplier)