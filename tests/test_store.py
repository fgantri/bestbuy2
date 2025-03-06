"""
Tests for the Store class.
"""
import unittest
from product import Product, NonStockedProduct, LimitedProduct
from store import Store


class TestStore(unittest.TestCase):
    """Test cases for the Store class."""
    
    def setUp(self):
        """Set up test fixtures for each test method."""
        # Create test products
        self.product1 = Product("MacBook", price=1000, quantity=5)
        self.product2 = Product("iPhone", price=800, quantity=10)
        self.limited_product = LimitedProduct("Shipping", price=10, quantity=5, maximum=1)
        self.non_stocked_product = NonStockedProduct("Windows License", price=125)
        
        # Create store with products
        self.store = Store([
            self.product1, 
            self.product2,
            self.limited_product,
            self.non_stocked_product
        ])
    
    def test_add_product(self):
        """Test adding products to the store."""
        new_product = Product("iPad", price=500, quantity=3)
        self.store.add_product(new_product)
        
        # Check if product was added by searching in the _products list
        found = False
        for product in self.store._products:
            if product.name == "iPad":
                found = True
                break
        self.assertTrue(found, "New product not found in store's products list")
    
    def test_remove_product(self):
        """Test removing products from the store."""
        initial_count = len(self.store._products)
        self.store.remove_product(self.product1.name)
        
        # Check if product was removed - count should be one less
        self.assertEqual(len(self.store._products), initial_count - 1)
        
        # Check that the product is not in the list
        for product in self.store._products:
            self.assertNotEqual(product.name, "MacBook", "Product should have been removed")
    
    def test_get_total_quantity(self):
        """Test getting total quantity of products in store."""
        # Total should be 5 + 10 + 5 + 0 = 20
        self.assertEqual(self.store.get_total_quantity(), 20)
        
        # Add a new product and check again
        new_product = Product("iPad", price=500, quantity=3)
        self.store.add_product(new_product)
        self.assertEqual(self.store.get_total_quantity(), 23)
    
    def test_order_success(self):
        """Test successful order processing."""
        shopping_list = [
            (self.product1, 2),  # 2 MacBooks
            (self.limited_product, 1),  # 1 Shipping (within limit)
            (self.non_stocked_product, 3)  # 3 Windows Licenses
        ]
        
        # Expected total: (2 * 1000) + (1 * 10) + (3 * 125) = 2010 + 375 = 2385
        total = self.store.order(shopping_list)
        
        # Verify total price
        self.assertEqual(total, 2385)
        
        # Verify quantities were reduced appropriately
        self.assertEqual(self.product1.get_quantity(), 3)  # 5 - 2 = 3
        self.assertEqual(self.limited_product.get_quantity(), 4)  # 5 - 1 = 4
        self.assertEqual(self.non_stocked_product.get_quantity(), 0)  # Non-stocked remains 0
    
    def test_order_fail_limited_product(self):
        """Test order failing due to limited product constraint."""
        shopping_list = [
            (self.product1, 2),  # 2 MacBooks
            (self.limited_product, 2)  # 2 Shipping (exceeds maximum of 1)
        ]
        
        # Initial quantities
        initial_macbook_qty = self.product1.get_quantity()
        initial_shipping_qty = self.limited_product.get_quantity()
        
        # Order should fail due to limited product constraint
        with self.assertRaises(Exception) as context:
            self.store.order(shopping_list)
        
        # Verify error message contains expected text
        self.assertIn("Cannot buy more than 1 of Shipping", str(context.exception))
        
        # Verify quantities were not reduced
        self.assertEqual(self.product1.get_quantity(), initial_macbook_qty)
        self.assertEqual(self.limited_product.get_quantity(), initial_shipping_qty)
    
    def test_order_fail_insufficient_quantity(self):
        """Test order failing due to insufficient quantity."""
        shopping_list = [
            (self.product1, 10),  # 10 MacBooks (more than available)
            (self.limited_product, 1)  # 1 Shipping
        ]
        
        # Initial quantities
        initial_macbook_qty = self.product1.get_quantity()
        initial_shipping_qty = self.limited_product.get_quantity()
        
        # Order should fail due to insufficient quantity
        with self.assertRaises(Exception) as context:
            self.store.order(shopping_list)
        
        # Verify error message contains expected text
        self.assertIn("Not enough MacBook in stock", str(context.exception))
        
        # Verify quantities were not reduced
        self.assertEqual(self.product1.get_quantity(), initial_macbook_qty)
        self.assertEqual(self.limited_product.get_quantity(), initial_shipping_qty)


if __name__ == '__main__':
    unittest.main()
