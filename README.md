# Best Buy Store Application

This is a simple Best Buy store application that allows users to manage products and apply promotions.

## Features

### Products
- Regular products with stock quantities
- Non-stocked products (e.g., digital products)
- Limited products with maximum purchase limits

### Promotions
The application supports the following promotion types:

1. **Percentage Discount** - Apply a percentage discount to a product (e.g., 20% off)
2. **Second Half Price** - Every second item is sold at half price
3. **Buy 2, Get 1 Free** - For every three items purchased, one is free

## Usage

Run the application with:

```
python main.py
```

The application provides a menu-based interface that allows you to:
1. List all products in the store
2. Show the total amount of items in the store
3. Make an order
4. Quit

## Promotion System

Each product can have one promotion applied to it at a time. Promotions affect the price calculation when products are purchased. The promotion system uses an abstract base class called `Promotion` with concrete implementations for each promotion type.
