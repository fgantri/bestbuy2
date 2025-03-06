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
        self.price = price
        
        self._quantity = quantity
        self._active = self._quantity > 0
        self._promotion: Optional[Promotion] = None

    @property
    def quantity(self) -> int:
        """Get the current quantity of the product."""
        return self._quantity
    
    def get_quantity(self) -> int:
        """
        Get the current quantity of the product.
        
        Returns:
            The current quantity.
        """
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        """
        Set the product quantity and update active status.
        
        Args:
            quantity: The new quantity.
        """
        self._quantity = quantity
        self._active = quantity > 0

    def is_active(self) -> bool:
        """
        Check if the product is active.
        
        Returns:
            True if product is active, False otherwise.
        """
        return self._active

    def activate(self) -> None:
        """Activate the product."""
        self._active = True

    def deactivate(self) -> None:
        """Deactivate the product."""
        self._active = False
    
    def get_promotion(self) -> Optional[Promotion]:
        """
        Get the current promotion applied to the product.
        
        Returns:
            The current promotion or None if no promotion is applied.
        """
        return self._promotion
    
    def set_promotion(self, promotion: Optional[Promotion]) -> None:
        """
        Set a promotion for the product.
        
        Args:
            promotion: The promotion to apply or None to remove.
        """
        self._promotion = promotion

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
            
        quantity_after_sale = self.get_quantity() - quantity
        if quantity_after_sale < 0:
            raise Exception(f"Not enough {self.name} in stock! Only {self.get_quantity()} left.")
        
        self.set_quantity(quantity_after_sale)
        
        # Apply promotion if available
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        
        return self.price * quantity

    def show(self) -> str:
        """
        Get a string representation of the product.
        
        Returns:
            A formatted string with product details.
        """
        promotion_str = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.get_quantity()}{promotion_str}"


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
        self._active = True  # Always active

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
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        
        return self.price * quantity

    def show(self) -> str:
        """
        Get a string representation of the non-stocked product.
        
        Returns:
            A formatted string with product details.
        """
        promotion_str = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited{promotion_str}"


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
            
        if quantity > self._maximum:
            raise Exception(f"Cannot buy more than {self._maximum} of {self.name} in a single order!")
        
        # Apply promotion if available
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        
        return super().buy(quantity)

    def show(self) -> str:
        """
        Get a string representation of the limited product.
        
        Returns:
            A formatted string with product details.
        """
        promotion_str = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: ${self.price}, Limited to {self._maximum} per order!{promotion_str}"
