import unittest

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order_line import OrderLine


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource", "sales@techsource.com")

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -5):
            with self.assertRaises(ValueError):
                PhysicalProduct("P001", "Lamp", bad_price, 5, self.supplier, 1.0)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            DigitalProduct("D001", "Editor", 10.0, -1, self.supplier, 100)

    def test_zero_stock_is_allowed(self):
        product = PhysicalProduct("P001", "Lamp", 10.0, 0, self.supplier, 1.0)
        self.assertEqual(product.get_stock(), 0)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        product = PhysicalProduct("P001", "Lamp", 10.0, 5, self.supplier, 1.0)
        for bad_quantity in (0, -3):
            with self.assertRaises(ValueError):
                OrderLine(product, bad_quantity)

    def test_both_subclasses_keep_the_same_stock_rule(self):
        physical = PhysicalProduct("P001", "Lamp", 10.0, 5, self.supplier, 1.0)
        digital = DigitalProduct("D001", "Editor", 10.0, 5, self.supplier, 100)
        for product in (physical, digital):
            self.assertFalse(product.update_stock(-1))
            self.assertEqual(product.get_stock(), 5)
            self.assertTrue(product.update_stock(8))
            self.assertEqual(product.get_stock(), 8)


if __name__ == "__main__":
    unittest.main()