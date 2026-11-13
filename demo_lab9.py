from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

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