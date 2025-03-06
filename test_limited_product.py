from product import LimitedProduct

# Create a limited product
shipping = LimitedProduct("Shipping", price=10, quantity=100, maximum=1)

print("Maximum limit:", shipping._maximum)
print("Product info:", shipping.show())

try:
    # This should work
    price = shipping.buy(1)
    print(f"Bought 1 for ${price}, remaining quantity: {shipping.get_quantity()}")
    
    # This should fail
    print("Trying to buy 2 (should fail)...")
    price = shipping.buy(2)
    print(f"Bought 2 for ${price}")  # We shouldn't reach this line
except Exception as e:
    print(f"Got expected exception: {e}")

# Create another limited product with a different maximum
express = LimitedProduct("Express Shipping", price=20, quantity=50, maximum=2)

try:
    # This should work
    price = express.buy(2)
    print(f"Bought 2 for ${price}, remaining quantity: {express.get_quantity()}")
    
    # This should fail
    print("Trying to buy 3 (should fail)...")
    price = express.buy(3)
    print(f"Bought 3 for ${price}")  # We shouldn't reach this line
except Exception as e:
    print(f"Got expected exception: {e}")
