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
        self._promotion = None

    def get_quantity(self):
        """Getter function for quantity :returns the quantity (float)."""
        return self._quantity

    def set_quantity(self, quantity):
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        if quantity <= 0:
            self._active = False
        else:
            self._active = True
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
    
    def get_promotion(self):
        """Getter function for promotion."""
        return self._promotion
    
    def set_promotion(self, promotion):
        """Setter function for promotion."""
        self._promotion = promotion

    def buy(self, quantity):
        """Buys a given quantity of the product :returns the total price (float) of the purchase."""
        quantity_after_sale = self.get_quantity() - quantity
        if quantity_after_sale < 0:
            raise Exception(f"Not enough {self.name} in stock! only {self.get_quantity()} left.")
        self.set_quantity(quantity_after_sale)
        
        # Apply promotion if available
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        else:
            return self.price * quantity

    def show(self):
        """Returns a string that represents the product,
        for example: 'MacBook Air M2, Price: 1450, Quantity: 100'"""
        promotion_str = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.get_quantity()}{promotion_str}"


class LimitedProduct(Product):

    instances = []

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self._maximum = maximum
        LimitedProduct.instances.append(self)

    def buy(self, quantity):
        ordered_quantity = sum([limited_product.get_quantity()
                                for limited_product in LimitedProduct.instances])
        if quantity > ordered_quantity:
            raise Exception(f"Only {self._maximum} is allowed from this {self.name}!")
        
        # Apply promotion if available
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        else:
            return super().buy(quantity)

    def show(self):
        """Returns a string that represents the product,
        for example: 'Shipping, Price: $10, Limited to 1 per order!'"""
        promotion_str = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: ${self.price}, Limited to {self._maximum} per order!{promotion_str}"


class NonStockedProduct(Product):

    def __init__(self, name, price):
        super().__init__(name, price, 0)
        self._active = True

    def buy(self, quantity):
        # Apply promotion if available
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        else:
            return self.price * quantity

    def show(self):
        """Returns a string that represents the product,
        for example: 'MacBook Air M2, Price: 1450, Quantity: Unlimited'"""
        promotion_str = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited{promotion_str}"
