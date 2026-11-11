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