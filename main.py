#!/usr/bin/env python3
"""
Best Buy Store Application

This is the main entry point for the Best Buy store application.
It sets up the store, products, and promotions, and provides a console interface for users.
"""

import sys
from typing import Dict, Tuple, Callable, List, Any

from product import Product, NonStockedProduct, LimitedProduct
from store import Store
import promotions


def setup_store() -> Store:
    """
    Set up the store with initial inventory and promotions.
    
    Returns:
        A store instance with products and promotions configured.
    """
    # Setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]
    
    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent
    
    return Store(product_list)


def main() -> int:
    """
    Best Buy store app main logic.
    
    Returns:
        Exit code (0 for success).
    """
    best_buy = setup_store()
    start(best_buy)
    return 0


def start(store: Store) -> None:
    """
    Start the store user interface and handle user interactions.
    
    Args:
        store: The store instance to operate on.
    """
    menu: Dict[int, Tuple[Callable[[], None], str]] = {
        1: (lambda: list_products(store), "List all products in store"),
        2: (lambda: print_store_amount(store), "Show total amount in store"),
        3: (lambda: make_order(store), "Make an order"),
        4: (None, "Quit")  # Using None as a sentinel value
    }

    while True:
        print_menu(menu)
        try:
            choice = int(input("Please choose a number: "))
            
            # Handle quit option directly
            if choice == 4:
                print("Thank you for shopping with us!")
                break
                
            command, _ = menu.get(choice, (None, None))
            
            if command is None:
                print("Invalid choice! Please try again.")
                continue
                
            command()
            
        except ValueError:
            print("Error with your choice! Please enter a number.")
        except KeyError:
            print("Invalid choice! Please try again.")
        except KeyboardInterrupt:
            print("\nExiting program...")
            break


def print_menu(menu: Dict[int, Tuple[Callable[[], Any], str]]) -> None:
    """
    Print the menu with available tasks to select.
    
    Args:
        menu: Dictionary mapping menu numbers to (function, label) pairs.
    """
    print("\nStore Menu")
    print("----------")
    for key, option in menu.items():
        _, label = option
        print(f"{key}. {label}")


def list_products(store: Store) -> None:
    """
    List all available products in the given store.
    
    Args:
        store: The store instance to list products from.
    """
    products = store.get_all_products()
    if not products:
        print("No active products in store!")
        return
        
    print("------")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.show()}")
    print("------")


def print_store_amount(store: Store) -> None:
    """
    Print the total amount of products available in the given store.
    
    Args:
        store: The store instance to get quantities from.
    """
    total = store.get_total_quantity()
    print(f"Total of {total} items in store")


def make_order(store: Store) -> None:
    """
    Run an order process from store until user confirms with empty input.
    
    Args:
        store: The store instance to order from.
    """
    shopping_list: List[Tuple[Product, int]] = []
    
    # Display available products
    list_products(store)
    print("When you want to finish order, enter empty text.")

    while True:
        try:
            product_key = input("Which product # do you want? ")
            
            # Quit ordering on empty input
            if not product_key:
                break
                
            amount = input("What amount do you want? ")
            
            # Quit ordering on empty input
            if not amount:
                break
                
            # Get the product and add to shopping list
            products = store.get_all_products()
            index = int(product_key) - 1
            
            if not 0 <= index < len(products):
                print(f"Invalid product number! Please enter 1-{len(products)}.")
                continue
                
            product = products[index]
            quantity = int(amount)
            
            if quantity <= 0:
                print("Please enter a positive quantity!")
                continue
                
            shopping_list.append((product, quantity))
            print("Product added to list!")
            
        except ValueError:
            print("Error: Please enter valid numbers!")
        except IndexError:
            print("Error: Invalid product selection!")

    # Process the order if we have items
    if shopping_list:
        try:
            total_payment = store.order(shopping_list)
            print(f"Order made! Total payment: ${total_payment:.2f}")
        except Exception as error:
            print(f"Error processing order: {error}")


if __name__ == "__main__":
    sys.exit(main())
