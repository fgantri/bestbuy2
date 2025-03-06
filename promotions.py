from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Avoid circular imports
if TYPE_CHECKING:
    from product import Product


class Promotion(ABC):
    """
    Abstract base class for all promotions.
    Defines the interface for applying promotions to products.
    """
    def __init__(self, name: str):
        """
        Initialize a promotion with a name.
        
        Args:
            name: The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Apply the promotion to a product purchase.
        
        Args:
            product: The product being purchased
            quantity: The quantity being purchased
            
        Returns:
            float: The total price after applying the promotion
        """
        pass


class PercentDiscount(Promotion):
    """
    A promotion that applies a percentage discount to the product price.
    Example: 20% off the regular price.
    """
    def __init__(self, name: str, percent: float):
        """
        Initialize a percentage discount promotion.
        
        Args:
            name: The name of the promotion.
            percent: The discount percentage (0-100).
            
        Raises:
            ValueError: If percent is not between 0 and 100.
        """
        super().__init__(name)
        if not 0 <= percent <= 100:
            raise ValueError("Percent discount must be between 0 and 100")
        self.percent = percent
        
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Apply a percentage discount to the product purchase.
        
        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.
            
        Returns:
            The discounted total price.
        """
        if quantity <= 0:
            return 0.0
            
        discount_multiplier = 1 - (self.percent / 100)
        return product.price * quantity * discount_multiplier


class SecondHalfPrice(Promotion):
    """
    A promotion where every second item is half price.
    Example: Buy one at full price, get the second at half price.
    """
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Apply a "second item half price" promotion to the product purchase.
        
        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.
            
        Returns:
            The discounted total price.
        """
        if quantity <= 0:
            return 0.0
            
        # Calculate how many full-price and half-price items
        full_price_count = (quantity + 1) // 2  # Ceiling division for odd quantities
        half_price_count = quantity // 2  # Floor division for even quantities
        
        total_price = (full_price_count * product.price) + (half_price_count * product.price * 0.5)
        return total_price


class ThirdOneFree(Promotion):
    """
    A promotion where every third item is free (Buy 2, Get 1 Free).
    Example: Buy two items, get the third one free.
    """
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Apply a "buy 2, get 1 free" promotion to the product purchase.
        
        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.
            
        Returns:
            The discounted total price.
        """
        if quantity <= 0:
            return 0.0
            
        # Calculate how many free items
        free_items = quantity // 3
        
        # Calculate how many paid items
        paid_items = quantity - free_items
        
        return paid_items * product.price
