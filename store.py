from typing import List, Tuple, Optional
from product import Product, NonStockedProduct


class Store:
    """
    Store class for managing products and processing orders.
    """
    def __init__(self, products: Optional[List[Product]] = None):
        """
        Initialize the store with a list of products.
        
        Args:
            products: List of products to initialize the store with.
        """
        self._products: List[Product] = [] if products is None else products

    def add_product(self, product: Product) -> None:
        """
        Add a product to the store.
        
        Args:
            product: The product to add.
        """
        self._products.append(product)

    def remove_product(self, product_name: str) -> None:
        """
        Remove a product from the store by name.
        
        Args:
            product_name: The name of the product to remove.
        """
        self._products = [product for product in self._products if product.name != product_name]

    def get_total_quantity(self) -> int:
        """
        Get the total quantity of all products in the store.
        
        Returns:
            The sum of all product quantities.
        """
        return sum(product.get_quantity() for product in self._products)

    def get_all_products(self) -> List[Product]:
        """
        Get all active products in the store.
        
        Returns:
            List of active products.
        """
        return [product for product in self._products if product.is_active()]

    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Process an order for products.
        
        Args:
            shopping_list: List of tuples containing (product, quantity).
            
        Returns:
            The total price of the order.
            
        Raises:
            Exception: If there's an issue with purchasing any product.
        """
        total = 0.0
        for product, quantity in shopping_list:
            # Find the actual product in the store's inventory
            for store_product in self._products:
                if product.name == store_product.name:
                    total += store_product.buy(quantity)
                    break
        return total
