from product import Product
from store import Store
import sys

def main():
    """bestbuy store app main logic"""
    # setup initial stock of inventory
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250)
                    ]
    best_buy = Store(product_list)
    start(best_buy)
    return 0


def start(store):
    """store user interface asks user for interaction until quit"""
    menu = {
        1: (lambda: list_products(store), "List all products in store"),
        2: (lambda: print_store_amount(store), "Show total amount in store"),
        3: (lambda: make_order(store), "Make an order"),
        4: (exit, "Quit")
    }

    while True:
        print_menu(menu)
        try:
            choice = int(input("Please choose a number: "))
            command = menu[choice][0]
            command()
        except ValueError:
            print("Error with your choice! Try again!")
            continue
        except KeyError:
            continue


def print_menu(menu):
    """prints menu with available tasks to select"""
    print("Store Menu")
    print("----------")
    for key, option in menu.items():
        _, label = option
        print(f"{key}. {label}")


def list_products(store):
    """lists all available products in given store"""
    print("------")
    for i, product in enumerate(store.get_all_products(), start=1):
        print(f"{i}. {product.name}, Price: ${product.price}, Quantity: {product.get_quantity()}")
    print("------")


def print_store_amount(store):
    """prints the total amount of products available in given store"""
    print(f"Total of {store.get_total_quantity()} items in store")


def make_order(store):
    """runs an order process from store until user confirms with empty input"""
    shopping_list = []
    list_products(store)
    print("When you want to finish order, enter empty text.")

    while True:
        try:
            product_key = input("Which product # do you want? ")
            amount = input("What amount do you want? ")

            # Quit ordering
            if product_key == "" or amount == "":

                if len(shopping_list) > 0:
                    try:
                        total_payment = store.order(shopping_list)
                    except ValueError as error_msg:
                        print(error_msg)
                        return
                    print(f"Order made! Total payment: {total_payment}")
                return

            product = store.get_all_products()[int(product_key) - 1]
            shopping_list.append((product, int(amount)))
            print("Product added to list!")
        except (ValueError, IndexError):
            print("Error adding product!")


if __name__ == "__main__":
    sys.exit(main())
