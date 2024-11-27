class Product:

    def __init__(self, name, price, quantity):
        """product constructor"""
        if name == "":
            raise Exception("product name cannot be empty!")
        self.name = name
        if price < 0:
            raise Exception("product price cannot be negative!")
        self.price = price
        self._quantity = quantity
        self._active = self._quantity > 0

    def get_quantity(self):
        """Getter function for quantity :returns the quantity (float)."""
        return self._quantity

    def set_quantity(self, quantity):
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        if quantity <= 0:
            self._active = False
        self._quantity = quantity

    def is_active(self):
        """Getter function for active :returns True if the product is active, otherwise False"""
        return self._active

    def activate(self):
        """Activates the product."""
        self._active = True

    def deactivate(self):
        """Deactivates the product."""
        self._active = False

    def buy(self, quantity):
        """Buys a given quantity of the product :returns the total price (float) of the purchase."""
        quantity_after_sale = self.get_quantity() - quantity
        if quantity_after_sale < 0:
            raise Exception(f"Not enough {self.name} in stock! only {self.get_quantity()} left.")
        self.set_quantity(quantity_after_sale)
        return self.price * quantity

    def show(self):
        """Returns a string that represents the product,
        for example: 'MacBook Air M2, Price: 1450, Quantity: 100'"""
        return f"{self.name}, Price: {self.price}, Quantity: {self.get_quantity()}"


def main():
    """main test function for products class"""
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())

    bose.set_quantity(1000)
    print(bose.show())


if __name__ == "__main__":
    main()
