from typing import Optional, Union
from promotions import Promotion


class Product:
    """
    Base Product class for store inventory items.
    """
    def __init__(self, name: str, price: float, quantity: int):
        """
        Initialize a product with name, price, and quantity.
        
        Args:
            name: The product name.
            price: The product price.
            quantity: The initial quantity in stock.
            
        Raises:
            Exception: If name is empty or price is negative.
        """
        if name == "":
            raise Exception("Product name cannot be empty!")
        self.name = name
        
        if price < 0:
            raise Exception("Product price cannot be negative!")
        self._price = price
        
        self._quantity = quantity
        self._active = self._quantity > 0
        self._promotion: Optional[Promotion] = None

    @property
    def price(self) -> float:
        """Get the product price."""
        return self._price
        
    @price.setter
    def price(self, value: float) -> None:
        """
        Set the product price.
        
        Args:
            value: The new price.
            
        Raises:
            Exception: If price is negative.
        """
        if value < 0:
            raise Exception("Product price cannot be negative!")
        self._price = value

    @property
    def quantity(self) -> int:
        """Get the current quantity of the product."""
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        """
        Set the product quantity and update active status.
        
        Args:
            value: The new quantity.
        """
        self._quantity = value
        self._active = value > 0

    @property
    def active(self) -> bool:
        """Check if the product is active."""
        return self._active
        
    @active.setter
    def active(self, value: bool) -> None:
        """Set the product active status."""
        self._active = value

    @property
    def promotion(self) -> Optional[Promotion]:
        """Get the current promotion applied to the product."""
        return self._promotion
        
    @promotion.setter
    def promotion(self, value: Optional[Promotion]) -> None:
        """
        Set a promotion for the product.
        
        Args:
            value: The promotion to apply or None to remove.
        """
        self._promotion = value
        
    # Keep is_active method for backward compatibility
    def is_active(self) -> bool:
        """
        Check if the product is active.
        
        Returns:
            True if the product is active, False otherwise.
        """
        return self.active

    def buy(self, quantity: int) -> float:
        """
        Buy a given quantity of the product.
        
        Args:
            quantity: The quantity to buy.
            
        Returns:
            The total price (with any applicable promotion).
            
        Raises:
            Exception: If there's not enough product in stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        quantity_after_sale = self.quantity - quantity
        if quantity_after_sale < 0:
            raise Exception(f"Not enough {self.name} in stock! Only {self.quantity} left.")
        
        self.quantity = quantity_after_sale
        
        # Apply promotion if available
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        
        return self.price * quantity

    def __str__(self) -> str:
        """
        Get a string representation of the product.
        
        Returns:
            A formatted string with product details.
        """
        promotion_str = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}{promotion_str}"
        
    def __gt__(self, other: 'Product') -> bool:
        """
        Compare if this product's price is greater than another product's price.
        
        Args:
            other: The other product to compare with.
            
        Returns:
            True if this product's price is greater, False otherwise.
        """
        return self.price > other.price
        
    def __lt__(self, other: 'Product') -> bool:
        """
        Compare if this product's price is less than another product's price.
        
        Args:
            other: The other product to compare with.
            
        Returns:
            True if this product's price is less, False otherwise.
        """
        return self.price < other.price
        
    # Keep the show method for backward compatibility
    def show(self) -> str:
        """
        Get a string representation of the product.
        
        Returns:
            A formatted string with product details.
        """
        return self.__str__()


class NonStockedProduct(Product):
    """
    Product type for non-physical items that don't have stock quantities.
    """
    def __init__(self, name: str, price: float):
        """
        Initialize a non-stocked product.
        
        Args:
            name: The product name.
            price: The product price.
        """
        super().__init__(name, price, 0)
        self.active = True  # Always active

    def buy(self, quantity: int) -> float:
        """
        Buy a given quantity of the non-stocked product.
        
        Args:
            quantity: The quantity to buy.
            
        Returns:
            The total price (with any applicable promotion).
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        # Apply promotion if available
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        
        return self.price * quantity

    def __str__(self) -> str:
        """
        Get a string representation of the non-stocked product.
        
        Returns:
            A formatted string with product details.
        """
        promotion_str = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited{promotion_str}"
        
    # Keep the show method for backward compatibility
    def show(self) -> str:
        """
        Get a string representation of the non-stocked product.
        
        Returns:
            A formatted string with product details.
        """
        return self.__str__()


class LimitedProduct(Product):
    """
    Product type with a maximum purchase limit per order.
    """
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initialize a limited product with a maximum purchase quantity.
        
        Args:
            name: The product name.
            price: The product price.
            quantity: The initial quantity in stock.
            maximum: The maximum quantity allowed per order.
        """
        super().__init__(name, price, quantity)
        self._maximum = maximum
        
    @property
    def maximum(self) -> int:
        """Get the maximum purchase quantity per order."""
        return self._maximum

    def buy(self, quantity: int) -> float:
        """
        Buy a given quantity of the limited product.
        
        Args:
            quantity: The quantity to buy.
            
        Returns:
            The total price (with any applicable promotion).
            
        Raises:
            Exception: If the quantity exceeds the maximum limit or if not enough in stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        if quantity > self.maximum:
            raise Exception(f"Cannot buy more than {self.maximum} of {self.name} in a single order!")
        
        # Apply promotion if available
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        
        return super().buy(quantity)

    def __str__(self) -> str:
        """
        Get a string representation of the limited product.
        
        Returns:
            A formatted string with product details.
        """
        promotion_str = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Limited to {self.maximum} per order!{promotion_str}"
        
    # Keep the show method for backward compatibility
    def show(self) -> str:
        """
        Get a string representation of the limited product.
        
        Returns:
            A formatted string with product details.
        """
        return self.__str__()
