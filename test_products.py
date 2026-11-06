from physical_product import PhysicalProduct
from digital_product import DigitalProduct

physical = PhysicalProduct("P001", "Guitar", 499.00, 5, 3.5)
digital = DigitalProduct("D001", "Operating System", 89.90, 100, 2500)

print("=== Display Information ===")
physical.display_information()
digital.display_information()

print("\n=== Fulfilment Info ===")
print(physical.get_fulfilment_info())
print(digital.get_fulfilment_info())

print("\n=== Abstract Class Test ===")
from product import Product
try:
    generic = Product("X001", "Generic", 10.0, 1)
except TypeError as error:
    print("Cannot instantiate Product:", error)