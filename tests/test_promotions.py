"""
Tests for the promotion system.
"""
import unittest
from product import Product
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


class TestPromotions(unittest.TestCase):
    """Test cases for the promotion system."""
    
    def setUp(self):
        """Set up test fixtures for each test method."""
        self.product = Product("Test Product", price=100, quantity=100)
        self.percent_discount = PercentDiscount("20% off", percent=20)
        self.second_half_price = SecondHalfPrice("Second Half Price")
        self.third_one_free = ThirdOneFree("Buy 2 Get 1 Free")

    def test_percent_discount(self):
        """Test PercentDiscount promotion."""
        self.product.promotion = self.percent_discount
        # 5 items with 20% discount should be 5 * 100 * 0.8 = 400
        self.assertEqual(self.product.buy(5), 400)

    def test_second_half_price(self):
        """Test SecondHalfPrice promotion."""
        self.product.promotion = self.second_half_price
        
        # 1 item: 1 full price = 100
        self.assertEqual(self.product.buy(1), 100)
        
        # 2 items: 1 full price + 1 half price = 100 + 50 = 150
        self.product.quantity = 100  # Reset quantity
        self.assertEqual(self.product.buy(2), 150)
        
        # 5 items: 3 full price + 2 half price = 300 + 100 = 400
        self.product.quantity = 100  # Reset quantity
        self.assertEqual(self.product.buy(5), 400)

    def test_third_one_free(self):
        """Test ThirdOneFree promotion."""
        self.product.promotion = self.third_one_free
        
        # 1 item: 1 paid = 100
        self.assertEqual(self.product.buy(1), 100)
        
        # 2 items: 2 paid = 200
        self.product.quantity = 100  # Reset quantity
        self.assertEqual(self.product.buy(2), 200)
        
        # 3 items: 2 paid + 1 free = 200
        self.product.quantity = 100  # Reset quantity
        self.assertEqual(self.product.buy(3), 200)
        
        # 7 items: 2*2 paid + 2 free + 1 paid = 500
        self.product.quantity = 100  # Reset quantity
        self.assertEqual(self.product.buy(7), 500)


if __name__ == '__main__':
    unittest.main()
