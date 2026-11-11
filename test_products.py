from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product

supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
physical = PhysicalProduct("P001", "Guitar", 499.00, 5, supplier, 3.5)
digital = DigitalProduct("D001", "Operating System", 89.90, 100, supplier, 2500)

print("=== Display Information ===")
physical.display_information()
digital.display_information()

print("\n=== Fulfilment Info ===")
print(physical.get_fulfilment_info())
print(digital.get_fulfilment_info())

print("\n=== Abstract Class Test ===")
try:
    generic = Product("X001", "Generic", 10.0, 1, supplier)
except TypeError as error:
    print("Cannot instantiate Product:", error)

print("\n=== Shipping Cost ===")
light = PhysicalProduct("P002", "Book", 20.00, 50, supplier, 0.5)
heavy = PhysicalProduct("P003", "Amplifier", 350.00, 3, supplier, 12)
print(f"{light.get_name()}: ${light.calculate_shipping_cost():.2f}")
print(f"{heavy.get_name()}: ${heavy.calculate_shipping_cost():.2f}")
print("Digital has shipping?", hasattr(digital, "calculate_shipping_cost"))