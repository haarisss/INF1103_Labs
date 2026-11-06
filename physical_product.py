from product import Product
from can_be_shipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"   Weight: {self.__weight} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."  
    
    def calculate_shipping_cost(self):
        # simple rule: $5 base fee + $2 per kg
        return 5.00 + 2.00 * self.__weight  
    