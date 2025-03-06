from product import Product, NonStockedProduct


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
            for i_product in self._products:
                if product.name == i_product.name:
                    total += i_product.buy(quantity)
        return total
