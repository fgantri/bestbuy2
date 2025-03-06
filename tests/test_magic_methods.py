#!/usr/bin/env python3
"""
Test script to verify magic methods implementation for the Best Buy store application.
"""
from product import Product, LimitedProduct, NonStockedProduct
from store import Store

def test_magic_methods():
    """Test the implementation of magic methods and properties."""
    print("Testing magic methods and properties...\n")
    
    # Setup initial stock of inventory
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)
    windows = NonStockedProduct("Windows License", price=125)
    
    # Create a store
    best_buy = Store([mac, bose])
    
    # Test price property and validation
    print("\n--- Testing price property setter validation ---")
    try:
        mac.price = -100  # Should give error
        print("❌ ERROR: Setting negative price should have raised an exception")
    except Exception as e:
        print(f"✅ PASS: Got expected exception: {e}")
    
    # Test __str__ magic method
    print("\n--- Testing __str__ magic method ---")
    expected_str = "MacBook Air M2, Price: $1450, Quantity: 100"
    actual_str = str(mac)
    if expected_str in actual_str:
        print(f"✅ PASS: {actual_str}")
    else:
        print(f"❌ ERROR: Expected '{expected_str}', got '{actual_str}'")
    
    # Test comparison operators
    print("\n--- Testing comparison operators (>, <) ---")
    if mac > bose:
        print("✅ PASS: MacBook is more expensive than Bose earbuds")
    else:
        print("❌ ERROR: Mac should be more expensive than Bose")
    
    if bose < mac:
        print("✅ PASS: Bose earbuds are less expensive than MacBook")
    else:
        print("❌ ERROR: Bose should be less expensive than Mac")
    
    # Test 'in' operator
    print("\n--- Testing 'in' operator ---")
    if mac in best_buy:
        print("✅ PASS: MacBook is in best_buy store")
    else:
        print("❌ ERROR: MacBook should be in best_buy store")
    
    if pixel in best_buy:
        print("❌ ERROR: Pixel should not be in best_buy store")
    else:
        print("✅ PASS: Pixel is not in best_buy store")
    
    # Test store addition
    print("\n--- Testing store addition ---")
    other_store = Store([pixel, windows])
    combined_store = best_buy + other_store
    
    combined_products = [p.name for p in combined_store._products]
    expected_products = ["MacBook Air M2", "Bose QuietComfort Earbuds", "Google Pixel 7", "Windows License"]
    
    if all(product in combined_products for product in expected_products):
        print("✅ PASS: Combined store has all expected products")
    else:
        print(f"❌ ERROR: Expected {expected_products}, got {combined_products}")
    
    print("\n--- Testing iteration through store ---")
    for product in best_buy:
        print(f"Iterating through product: {product.name}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_magic_methods()
