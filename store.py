from product import Product

class Store:

    def __init__(self, products):
        """store constructor"""
        self._products: [Product] = [] if products is None else products

    def add_product(self, product):
        """Adds a product to store."""
        self._products.append(product)

    def remove_product(self, product_name):
        """Removes a product from store."""
        self._products = [product_name != product.name for product in self._products]

    def get_total_quantity(self):
        """Returns how many items are in the store in total."""
        return sum([product.get_quantity() for product in self._products])

    def get_all_products(self):
        """Returns all products in the store that are active."""
        return [product for product in self._products if product.is_active()]

    def order(self, shopping_list):
        """Buys the products and returns the total price of the order."""
        total = 0
        for product, quantity in shopping_list:
            for i_product in self.get_all_products():
                if i_product.name == product.name:
                    if quantity > i_product.get_quantity():
                        raise ValueError("Error while making order! Quantity larger than what exists")
                    i_product.set_quantity(product.get_quantity() - quantity)
            total += product.price * quantity
        return total


def main():
    """main test function for store class"""
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    ]

    store = Store(product_list)
    products = store.get_all_products()
    print(store.get_total_quantity())
    print(store.order([(products[0], 1), (products[1], 2)]))
    for product in products:
        print(product.get_quantity())


if __name__ == "__main__":
    main()
