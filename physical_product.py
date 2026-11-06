from product import Product


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        print(f"ID: {self.get_product_id()} | Name: {self.get_name()} | "
              f"Price: ${self.get_price():.2f} | Stock: {self.get_stock()} | "
              f"Weight: {self.__weight} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data