import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource", "sales@techsource.com")

    def test_creates_a_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10,
                                        self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 1.2)

    def test_creates_a_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100,
                                        self.supplier, 350)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 350)

    def test_everything_returned_is_a_product(self):
        for product_type in ("physical", "digital"):
            product = ProductFactory.create(product_type, "X1", "Item", 10.0, 1,
                                            self.supplier)
            self.assertIsInstance(product, Product)

    def test_unknown_type_raises_value_error_with_clear_message(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Install", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type: service", str(context.exception))


if __name__ == "__main__":
    unittest.main()