from typing import List, Tuple, Optional
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
            if isinstance(store_product, LimitedProduct) and hasattr(store_product, '_maximum'):
                if quantity > store_product._maximum:
                    raise Exception(f"Cannot buy more than {store_product._maximum} of {name} in a single order!")
            
            # Check if it's a regular product with insufficient quantity
            if not isinstance(store_product, NonStockedProduct):
                if store_product.get_quantity() < quantity:
                    raise Exception(f"Not enough {name} in stock! Only {store_product.get_quantity()} left.")
        
        # Now process the actual purchase
        total = 0.0
        for name, store_product in store_products.items():
            quantity = order_quantities[name]
            
            # For non-stocked products, don't reduce quantity
            if isinstance(store_product, NonStockedProduct):
                if store_product._promotion:
                    total += store_product._promotion.apply_promotion(store_product, quantity)
                else:
                    total += store_product.price * quantity
            else:
                # For regular and limited products, reduce quantity and calculate price
                current_quantity = store_product.get_quantity()
                store_product.set_quantity(current_quantity - quantity)
                
                if store_product._promotion:
                    total += store_product._promotion.apply_promotion(store_product, quantity)
                else:
                    total += store_product.price * quantity
        
        return total
