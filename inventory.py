from product import Product


class Inventory:
    def __init__(self) -> None:
        # aggregation: holds references to Products it does not own
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False  # duplicate ID
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)  # only removes the reference
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("------------------------------------------------")
        for product in self.__products:
            product.display_information()
        print("------------------------------------------------")

    def get_products(self) -> list[Product]:
        return list(self.__products)  # copy, so the internal list stays protected

# I have added added and checked for type hints across my codes