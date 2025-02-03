from decimal import Decimal

from apps.cart.models import Cart

class CartProcessor:
    def __init__(self, cart:Cart):
        self.cart = cart

    def calculate_total_price(self) -> Decimal:
        total_price = 0
        cart_products = self.cart.cartproduct_set.all()

        for cart_product in cart_products:
            product_price = cart_product.product.price
            quantity = cart_product.quantity
            discount = cart_product.discount
            total_price += product_price * (1 - discount / 100) * quantity

        return Decimal(total_price)
