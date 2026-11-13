import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from input_helpers import get_positive_float
from product_loader import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_and_capture(function, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):
    def test_keeps_asking_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            value, output = run_and_capture(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]):
            value, _ = run_and_capture(get_positive_float, "Price: ")
        self.assertEqual(value, 3.0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource", "sales@techsource.com")
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")
        with open(self.path, "w", newline="") as file:
            file.write(CSV_TEXT)

    def tearDown(self) -> None:
        self.folder.cleanup()

    def test_good_rows_load_and_bad_rows_are_skipped(self):
        inventory = Inventory()
        _, output = run_and_capture(load_products, self.path, inventory, self.supplier)
        self.assertEqual(len(inventory.get_products()), 3)
        self.assertIn("3 products loaded.", output)
        self.assertIn("Unknown product type: service", output)
        self.assertIn("Load attempt finished.", output)

    def test_missing_file_is_handled_without_crashing(self):
        inventory = Inventory()
        missing = os.path.join(self.folder.name, "nope.csv")
        _, output = run_and_capture(load_products, missing, inventory, self.supplier)
        self.assertEqual(len(inventory.get_products()), 0)
        self.assertIn("Products file not found", output)
        self.assertNotIn("products loaded", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()