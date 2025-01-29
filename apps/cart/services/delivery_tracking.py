from apps.cart.models import Cart


class DeliveryTracking:
    def __init__(self, cart: Cart):
        self.cart = cart
        self.delivery_type = cart.delivery_type
        self.delivery_type_methods_mapping = {
            'pickup': self.track_pickup,
            'nova_poshta': self.track_nova_poshta,
            'nova_poshta_courier': self.track_nova_poshta_courier,
            'nova_poshta_self': self.track_nova_poshta_self,
            'ukr_poshta': self.track_ukr_poshta,
        }

    def track_delivery(self):
        try:
            delivery_method = self.delivery_type_methods_mapping[self.delivery_type]
            delivery_method()
            self.notify_user()  # Користувач повинен бути сповіщений про статус доставки лише коли щось зміниться
        except KeyError:
            raise ValueError('Unknown delivery type')

    def notify_user(self):
        print('User has been notified about delivery status')

    def track_pickup(self):
        print('Tracking pickup')
        return True

    def track_nova_poshta(self):
        print('Tracking Nova Poshta')
        return True

    def track_nova_poshta_courier(self):
        print('Tracking Nova Poshta Courier')
        return True

    def track_nova_poshta_self(self):
        print('Tracking Nova Poshta Self')
        return True

    def track_ukr_poshta(self):
        print('Tracking Ukr Poshta')
        return True
