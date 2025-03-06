from abc import ABC, abstractmethod

class Promotion(ABC):
    """
    Abstract base class for all promotions.
    """
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
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
    """
    def __init__(self, name, percent):
        super().__init__(name)
        if not 0 <= percent <= 100:
            raise ValueError("Percent discount must be between 0 and 100")
        self.percent = percent
        
    def apply_promotion(self, product, quantity):
        discount_multiplier = 1 - (self.percent / 100)
        return product.price * quantity * discount_multiplier


class SecondHalfPrice(Promotion):
    """
    A promotion where every second item is half price.
    """
    def apply_promotion(self, product, quantity):
        # Calculate how many full-price and half-price items
        full_price_count = (quantity + 1) // 2  # Ceiling division for odd quantities
        half_price_count = quantity // 2  # Floor division for even quantities
        
        total_price = (full_price_count * product.price) + (half_price_count * product.price * 0.5)
        return total_price


class ThirdOneFree(Promotion):
    """
    A promotion where every third item is free (Buy 2, Get 1 Free).
    """
    def apply_promotion(self, product, quantity):
        # Calculate how many free items
        free_items = quantity // 3
        
        # Calculate how many paid items
        paid_items = quantity - free_items
        
        return paid_items * product.price
