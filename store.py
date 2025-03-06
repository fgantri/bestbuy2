from typing import List, Tuple, Optional, Iterator
from product import Product, NonStockedProduct, LimitedProduct


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
        return sum(product.quantity for product in self._products)

    def get_all_products(self) -> List[Product]:
        """
        Get all active products in the store.
        
        Returns:
            List of active products.
        """
        return [product for product in self._products if product.active]

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
        # Validate the entire order first
        store_products = {}  # Map from product name to actual store product
        order_quantities = {}  # Map to track quantity ordered for each product
        
        # Find all products in the store's inventory
        for product, quantity in shopping_list:
            found = False
            for store_product in self._products:
                if product.name == store_product.name:
                    store_products[product.name] = store_product
                    order_quantities[product.name] = quantity
                    found = True
                    break
            
            if not found:
                raise Exception(f"Product '{product.name}' not found in store inventory")
        
        # Verify all products can be purchased in the requested quantities
        for name, store_product in store_products.items():
            quantity = order_quantities[name]
            
            # Check if it's a LimitedProduct with quantity > maximum
            if isinstance(store_product, LimitedProduct):
                if quantity > store_product.maximum:
                    raise Exception(f"Cannot buy more than {store_product.maximum} of {name} in a single order!")
            
            # Check if it's a regular product with insufficient quantity
            if not isinstance(store_product, NonStockedProduct):
                if store_product.quantity < quantity:
                    raise Exception(f"Not enough {name} in stock! Only {store_product.quantity} left.")
        
        # Now process the actual purchase
        total = 0.0
        for name, store_product in store_products.items():
            quantity = order_quantities[name]
            
            # For non-stocked products, don't reduce quantity
            if isinstance(store_product, NonStockedProduct):
                if store_product.promotion:
                    total += store_product.promotion.apply_promotion(store_product, quantity)
                else:
                    total += store_product.price * quantity
            else:
                # For regular and limited products, reduce quantity and calculate price
                if store_product.promotion:
                    total += store_product.promotion.apply_promotion(store_product, quantity)
                else:
                    total += store_product.price * quantity
                
                # Reduce quantity after calculating price
                store_product.quantity = store_product.quantity - quantity
        
        return total
        
    def __contains__(self, product: Product) -> bool:
        """
        Check if a product exists in the store.
        
        Args:
            product: The product to check.
            
        Returns:
            True if product exists in store, False otherwise.
        """
        for store_product in self._products:
            if store_product.name == product.name:
                return True
        return False
        
    def __add__(self, other: 'Store') -> 'Store':
        """
        Combine two stores into a new store.
        
        Args:
            other: The other store to combine with.
            
        Returns:
            A new store containing products from both stores.
        """
        # Create a new store with products from this store
        new_products = list(self._products)
        
        # Add products from other store
        for product in other._products:
            found = False
            for existing_product in new_products:
                if existing_product.name == product.name:
                    found = True
                    break
            
            if not found:
                new_products.append(product)
                
        return Store(new_products)
        
    def __iter__(self) -> Iterator[Product]:
        """
        Create an iterator for the store's products.
        
        Returns:
            An iterator over the products in the store.
        """
        return iter(self._products)
