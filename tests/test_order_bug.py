"""
Tests for verifying the fix for the order bug where quantities were reduced
even when an order failed due to exceeding limits on limited products.
"""
import unittest
from product import Product, LimitedProduct
from store import Store


class TestOrderBugFix(unittest.TestCase):
    """Test case for verifying the fix for the order bug."""
    
    def test_quantities_not_reduced_on_order_failure(self):
        """Test that product quantities aren't reduced when an order fails."""
        # Create test products
        macbook = Product("MacBook", price=1000, quantity=5)
        shipping = LimitedProduct("Shipping", price=10, quantity=5, maximum=1)
        
        # Create store with products
        store = Store([macbook, shipping])
        
        # Initial quantities
        initial_macbook_qty = macbook.quantity
        initial_shipping_qty = shipping.quantity
        
        # Create a shopping list with valid items and one that exceeds limit
        shopping_list = [
            (macbook, 2),    # This is valid
            (shipping, 2)    # This exceeds maximum (1)
        ]
        
        # Try to place the order - should fail
        with self.assertRaises(Exception) as context:
            store.order(shopping_list)
            
        # Verify error message is about the limit
        self.assertIn("Cannot buy more than 1 of Shipping", str(context.exception))
        
        # Verify that quantities weren't reduced
        self.assertEqual(macbook.quantity, initial_macbook_qty)
        self.assertEqual(shipping.quantity, initial_shipping_qty)
    
    def test_quantities_reduced_on_order_success(self):
        """Test that quantities are properly reduced when an order succeeds."""
        # Create test products
        macbook = Product("MacBook", price=1000, quantity=5)
        shipping = LimitedProduct("Shipping", price=10, quantity=5, maximum=1)
        
        # Create store with products
        store = Store([macbook, shipping])
        
        # Create a valid shopping list
        shopping_list = [
            (macbook, 2),    # Valid
            (shipping, 1)    # Valid (within limit)
        ]
        
        # Place the order - should succeed
        total = store.order(shopping_list)
        
        # Verify order total (2000 + 10 = 2010)
        self.assertEqual(total, 2010)
        
        # Verify quantities were reduced
        self.assertEqual(macbook.quantity, 3)  # 5 - 2 = 3
        self.assertEqual(shipping.quantity, 4)  # 5 - 1 = 4


if __name__ == '__main__':
    unittest.main()
