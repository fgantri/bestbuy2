"""
Tests for the Product class.
"""
import unittest
from product import Product


class TestProduct(unittest.TestCase):
    """Test cases for the Product class."""
    
    def test_init_product(self):
        """Test that creating a normal product works."""
        p1_name, p2_name = "Playstation 5", "Samsung Odyssey G9"
        p1 = Product(name=p1_name, price=450, quantity=100)
        p2 = Product(name=p2_name, price=1100, quantity=50)
        p3 = p1
        
        self.assertEqual(p1.name, p1_name)
        self.assertEqual(p2.name, p2_name)
        self.assertIsNot(p1, p2)
        self.assertIs(p1, p3)

    def test_failed_init_product(self):
        """Test that creating a product with invalid details
        (empty name, negative price) invokes an exception."""
        # empty name
        with self.assertRaises(Exception):
            Product(name="", price=150, quantity=10)
        # negative price
        with self.assertRaises(Exception):
            Product(name="IPhone 16 Pro Max", price=-1150, quantity=10)

    def test_product_becomes_inactive(self):
        """Test that when a product reaches 0 quantity, it becomes inactive."""
        p1 = Product(name="IPhone 16 Pro Max", price=1150, quantity=10)
        self.assertTrue(p1.is_active())
        
        p1.quantity = 0
        self.assertFalse(p1.is_active())
        
        p1.quantity = -1
        self.assertFalse(p1.is_active())
        
        p1.quantity = -100
        self.assertFalse(p1.is_active())
        
        p1.quantity = 1
        self.assertTrue(p1.is_active())

    def test_product_purchase(self):
        """Test that product purchase modifies the quantity and returns the right output."""
        p1 = Product(name="IPhone 16 Pro Max", price=1150, quantity=10)
        self.assertEqual(p1.buy(7), 7 * p1.price)
        self.assertTrue(p1.is_active())
        
        self.assertEqual(p1.buy(3), 3 * p1.price)
        self.assertFalse(p1.is_active())

    def test_product_purchase_larger_amount(self):
        """Test that buying a larger quantity than exists invokes exception."""
        p1 = Product(name="IPhone 16 Pro Max", price=1150, quantity=10)
        with self.assertRaises(Exception):
            p1.buy(11)
        with self.assertRaises(Exception):
            p1.buy(110)
        
        self.assertEqual(p1.buy(10), p1.price * 10)


if __name__ == '__main__':
    unittest.main()
