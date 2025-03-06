"""
Tests for the different product types (NonStockedProduct, LimitedProduct).
"""
import unittest
from product import Product, NonStockedProduct, LimitedProduct


class TestProductTypes(unittest.TestCase):
    """Test cases for the different product type classes."""

    def test_non_stocked_product(self):
        """Test NonStockedProduct class functionality."""
        # Create a non-stocked product
        windows = NonStockedProduct("Windows License", price=125)
        
        # Verify it has zero quantity but is active
        self.assertEqual(windows.quantity, 0)
        self.assertTrue(windows.is_active())
        
        # Verify we can buy it without affecting quantity
        price = windows.buy(5)
        self.assertEqual(price, 125 * 5)
        self.assertEqual(windows.quantity, 0)
        
        # Verify show() displays properly
        self.assertIn("Unlimited", windows.show())

    def test_limited_product(self):
        """Test LimitedProduct with single maximum limit."""
        # Create a limited product with maximum 1
        shipping = LimitedProduct("Shipping", price=10, quantity=100, maximum=1)
        
        # Verify we can buy within the limit
        price = shipping.buy(1)
        self.assertEqual(price, 10)
        self.assertEqual(shipping.quantity, 99)
        
        # Verify we cannot buy more than the maximum
        with self.assertRaises(Exception):
            shipping.buy(2)
        
        # Verify show() displays properly
        self.assertIn("Limited to 1", shipping.show())
        
    def test_multiple_limited_products(self):
        """Test multiple LimitedProduct instances with different maximum limits."""
        # Create two different limited products
        shipping1 = LimitedProduct("Shipping Standard", price=10, quantity=100, maximum=1)
        shipping2 = LimitedProduct("Shipping Express", price=20, quantity=100, maximum=2)
        
        # Verify each has its own independent maximum
        shipping1.buy(1)  # Should work
        with self.assertRaises(Exception):
            shipping1.buy(2)  # Should fail (max 1)
            
        shipping2.buy(2)  # Should work (max 2)
        with self.assertRaises(Exception):
            shipping2.buy(3)  # Should fail (max 2)


if __name__ == '__main__':
    unittest.main()
