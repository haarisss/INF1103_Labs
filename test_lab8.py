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