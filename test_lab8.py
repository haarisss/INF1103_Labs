from product import Product
from order import Order
from inventory import Inventory
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# ---------- Section 2: Association ----------
print("=== Association: Supplier and Product ===")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
guitar = PhysicalProduct("P001", "Guitar", 499.00, 5, supplier, 3.5)
os_product = DigitalProduct("D001", "Operating System", 89.90, 100, supplier, 2500)

print("Supplier of the guitar:")
guitar.get_supplier().display_information()
print("Supplier of the operating system:")
os_product.get_supplier().display_information()
print("Same Supplier object?", guitar.get_supplier() is os_product.get_supplier())

del supplier  # only removes the variable name, not the object
print("\nAfter 'del supplier':")
guitar.get_supplier().display_information()

# ---------- Section 3: Aggregation ----------
print("\n=== Aggregation: Inventory and Product ===")
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(guitar)
print("Inventory A:")
inventory_a.display_all()

inventory_a.remove_product("P001")
print("Removed from Inventory A. Inventory A now:")
inventory_a.display_all()
print("Product still works on its own:")
guitar.display_information()

inventory_b.add_product(guitar)
print("Added to Inventory B. Inventory B:")
inventory_b.display_all()
print("Same Product object in B?", inventory_b.find_product("P001") is guitar)

# ---------- Section 4: Composition ----------
print("\n=== Composition: Order and OrderLine ===")
order1 = Order("O001")
order1.add_order_line(guitar, 1)
order1.add_order_line(os_product, 2)
order1.display_order()

order2 = Order("O002")
order2.add_order_line(guitar, 3)

line1 = order1.get_order_lines()[0]
line2 = order2.get_order_lines()[0]
print("\nSame Product object in both orders?", line1.get_product() is line2.get_product())
print("Same OrderLine object in both orders?", line1 is line2)
print("OrderLine ids:", id(line1), id(line2))

order1.remove_order_line("D001")
print("\nAfter removing the digital line from O001:")
order1.display_order()
print("The Product still exists:", os_product.get_name())

# ---------- Section 5: LSP ----------
print("\n=== LSP: show_product_details ===")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


show_product_details(guitar)
show_product_details(os_product)

print("\nupdate_stock behaves the same for both subclasses:")
for item in (guitar, os_product):
    print(item.get_name(), "-> update to 10:", item.update_stock(10),
          "| update to -1:", item.update_stock(-1), "| stock now:", item.get_stock())
    

# ---------- Section 6: Polymorphism ----------
print("\n=== Polymorphism: one loop, both product types ===")
inventory = Inventory()
inventory.add_product(guitar)
inventory.add_product(os_product)
for product in inventory.get_products():
    product.display_information()
    print(product.get_fulfilment_info())