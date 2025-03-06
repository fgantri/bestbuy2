# Best Buy Store Application

This is a command-line store application that simulates a Best Buy store interface. It allows managing products, applying promotions, and processing orders.

## Features

### Products

The application supports three types of products:

1. **Regular Products** - Physical products with stock quantities
2. **Non-stocked Products** - Digital products with unlimited availability (e.g., software licenses)
3. **Limited Products** - Products with a maximum purchase limit per order (e.g., shipping)

### Promotions

The application supports the following promotion types:

1. **Percentage Discount** - Apply a percentage discount to a product (e.g., 20% off)
2. **Second Half Price** - Every second item is sold at half price
3. **Buy 2, Get 1 Free** - For every three items purchased, one is free

## Code Structure

- `main.py` - Entry point for the application with the UI logic
- `store.py` - Store class for managing products and processing orders
- `product.py` - Product classes (base and specialized types)
- `promotions.py` - Promotion classes (abstract base class and implementations)

## Usage

### Requirements

- Python 3.7 or higher

### Running the Application

```bash
python main.py
```

The application provides a menu-based interface that allows you to:

1. List all products in the store
2. Show the total amount of items in the store
3. Make an order
4. Quit

## Design Patterns

The application uses several object-oriented design patterns:

- **Inheritance** - Product specializations extend the base Product class
- **Strategy Pattern** - Promotions are interchangeable strategies for calculating prices
- **Factory Method** - Store setup uses a factory method to create products and promotions
- **Composition** - Products have promotions composed into them

## Adding New Features

### Adding a New Product Type

To add a new product type, extend the `Product` class and override relevant methods:

```python
class NewProductType(Product):
    def __init__(self, name, price, quantity, extra_param):
        super().__init__(name, price, quantity)
        self._extra_param = extra_param
        
    def buy(self, quantity):
        # Custom buying logic
        return super().buy(quantity)
```

### Adding a New Promotion Type

To add a new promotion, extend the `Promotion` abstract class:

```python
class NewPromotion(Promotion):
    def __init__(self, name, param):
        super().__init__(name)
        self.param = param
        
    def apply_promotion(self, product, quantity):
        # Custom price calculation
        return calculated_price
```
