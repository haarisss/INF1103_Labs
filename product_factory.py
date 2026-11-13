from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra_value: float = 0.0) -> Product:
        # extra_value is the weight (kg) for a physical product,
        # or the download size (MB) for a digital product
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, extra_value)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, extra_value)
        else:
            raise ValueError(f"Unknown product type: {product_type}")