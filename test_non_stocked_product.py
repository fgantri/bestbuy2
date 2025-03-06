from product import NonStockedProduct

# Create a non-stocked product
windows = NonStockedProduct("Windows License", price=125)

print("Initial quantity:", windows.get_quantity())
print("Is active?", windows.is_active())
print("Product info:", windows.show())

# Buy the product multiple times
for quantity in [1, 5, 10]:
    price = windows.buy(quantity)
    print(f"Bought {quantity} for ${price}, quantity after purchase: {windows.get_quantity()}")
