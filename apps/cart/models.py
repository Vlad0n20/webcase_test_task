from django.db import models

from abstract.models import BaseModel, WhoDidIt

class CartProduct(BaseModel, WhoDidIt):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Cart Product'
        verbose_name_plural = 'Cart Products'
        ordering = ['cart', 'product']

    def __str__(self):
        return f'{self.cart} - {self.product}'


class Cart(BaseModel, WhoDidIt):
    class CartStatusChoices(models.TextChoices):
        CREATED = 'created', 'Created'
        INACTIVE = 'inactive', 'Inactive'
        ORDERED = 'ordered', 'Ordered'
        PAID = 'paid', 'Paid'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'

    class DeliveryTypeChoices(models.TextChoices):
        PICKUP = 'pickup', 'Pickup'
        DELIVERY = 'delivery', 'Delivery'
        NOVA_POSHTA = 'nova_poshta', 'Nova Poshta'
        NOVA_POSHTA_COURIER = 'nova_poshta_courier', 'Nova Poshta Courier'
        NOVA_POSHSHTA_SELF = 'nova_poshta_self', 'Nova Poshta Self' # поштомат
        UKR_POSHTA = 'ukr_poshta', 'Ukr Poshta'

    class PaymentTypeChoices(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'
        CASHLESS = 'cashless', 'Cashless'
        NOVA_PAY = 'nova_pay', 'Nova Pay'
        CASH_ON_DELIVERY  = 'cash_on_delivery', 'Cash on delivery'
        CRYPTO = 'crypto', 'Crypto'

    products = models.ManyToManyField('product.Product', through=CartProduct, related_name='carts')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=255, choices=CartStatusChoices.choices, default=CartStatusChoices.CREATED)
    delivery_type = models.CharField(max_length=255, choices=DeliveryTypeChoices.choices)
    delivery_address = models.CharField(max_length=255, null=True, blank=True)
    payment_type = models.CharField(max_length=255, choices=PaymentTypeChoices.choices)

    # стосовно знижок
    # Логіка по якій рахується знижка не була чітко визначена, накидав приблизно (через обмеженні в часі)
    # З фронту приходить, оскілький вона там точно має бути, бо її треба показати користувачу

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ['id']