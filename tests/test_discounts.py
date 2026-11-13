import unittest

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)


class HalfPrice(DiscountStrategy):
    """A brand-new strategy, defined without touching Order."""
    def apply(self, total: float) -> float:
        return total / 2


class TestDiscounts(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "TechSource", "sales@techsource.com")
        self.product = PhysicalProduct("P001", "Chair", 250.00, 5, supplier, 8.0)

    def make_order(self) -> Order:
        order = Order("O001")
        order.add_order_line(self.product, 1)  # total 250
        return order

    def test_no_discount_is_the_default(self):
        self.assertEqual(self.make_order().calculate_total(), 250.00)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.00)

    def test_bulk_discount_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(100), 95.00)

    def test_order_total_goes_through_the_strategy(self):
        order = self.make_order()
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_strategy_can_be_changed_with_set_discount(self):
        order = self.make_order()
        order.set_discount(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.00)

    def test_new_strategy_works_without_changing_order(self):
        order = Order("O002", HalfPrice())
        order.add_order_line(self.product, 1)
        self.assertEqual(order.calculate_total(), 125)

    def test_strategy_can_be_shared_by_two_orders(self):
        shared = PercentageDiscount(10)
        first, second = self.make_order(), self.make_order()
        first.set_discount(shared)
        second.set_discount(shared)
        self.assertEqual(first.calculate_total(), second.calculate_total())


if __name__ == "__main__":
    unittest.main()