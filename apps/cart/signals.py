from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Cart

@receiver(post_save, sender=Cart)
def send_order_to_another_service(sender, instance, created, **kwargs):
    if created:
        print('Order has been sent to another service')
        pass
    else:
        print('Order has been updated in another service')
        pass

@receiver(post_save, sender=Cart)
def notify_user_about_order_status_change(sender, instance, created, **kwargs):
    if not created and instance.status != instance.previous('status'):
        print('User has been notified about order status change')
        pass
