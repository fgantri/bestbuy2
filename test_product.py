import pytest
import product

def test_init_product():
    """Test that creating a normal product works."""
    p1_name, p2_name = "Playstation 5", "Samsung Odyssey G9"
    p1 = product.Product(name=p1_name, price=450, quantity=100)
    p2 = product.Product(name=p2_name, price=1100, quantity=50)
    p3 = p1
    assert p1.name == p1_name
    assert p2.name == p2_name
    assert p1 is not p2
    assert p1 is p3


def test_failed_init_product():
    """Test that creating a product with invalid details
    (empty name, negative price) invokes an exception."""
    # empty name
    with pytest.raises(Exception):
        product.Product(name="", price=150, quantity=10)
    # negative price
    with pytest.raises(Exception):
        product.Product(name="IPhone 16 Pro Max", price=-1150, quantity=10)


def test_product_becomes_inactive():
    """Test that when a product reaches 0 quantity, it becomes inactive."""
    p1 = product.Product(name="IPhone 16 Pro Max", price=1150, quantity=10)
    assert p1.is_active() == True
    p1.set_quantity(0)
    assert p1.is_active() == False
    p1.set_quantity(-1)
    assert p1.is_active() == False
    p1.set_quantity(-100)
    assert p1.is_active() == False
    p1.set_quantity(1)
    assert p1.is_active() == True


def test_product_purchase():
    """Test that product purchase modifies the quantity and returns the right output."""
    p1 = product.Product(name="IPhone 16 Pro Max", price=1150, quantity=10)
    assert p1.buy(7) == 7 * p1.price
    assert p1.is_active() == True
    assert p1.buy(3) == 3 * p1.price
    assert p1.is_active() == False


def test_product_purchase_larger_amount():
    """Test that buying a larger quantity than exists invokes exception."""
    p1 = product.Product(name="IPhone 16 Pro Max", price=1150, quantity=10)
    with pytest.raises(Exception):
        p1.buy(11)
    with pytest.raises(Exception):
        p1.buy(110)
    assert p1.buy(10) == p1.price * 10