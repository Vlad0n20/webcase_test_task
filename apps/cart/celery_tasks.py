from celery import shared_task

from apps.cart.models import Cart
from apps.cart.services.delivery_tracking import DeliveryTracking

@shared_task
def delivery_tracking():
    carts = Cart.objects.filter(status__in=[
        Cart.CartStatusChoices.PAID,
    ])
    for item in carts:
        delivery = DeliveryTracking(item)
        delivery.track_delivery()