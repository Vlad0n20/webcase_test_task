from apps.cart.models import Cart

class PaymentProcessor:

    def __init__(self, cart: Cart, payment_data: dict):
        self.cart = cart
        self.payment_type = cart.payment_type
        self.payment_data = payment_data

    def process_payment(self):
        payment_type_mapping = {
            'cash': self.process_cash_payment,
            'card': self.process_card_payment,
            'cashless': self.process_cash_less_payment,
            'crypto': self.process_cash_less_payment,
            'cash_on_delivery': self.process_cash_on_delivery_payment,
        }
        try:
            payment_method = payment_type_mapping[self.payment_type]
            payment_method()
            self.post_payment_process()
            self.notify_user()
        except KeyError:
            raise ValueError('Unknown payment type')

    def process_cash_payment(self):
        print('Processing cash payment')
        return True

    def process_card_payment(self):
        print('Processing card payment')
        return True

    def process_cash_less_payment(self):
        print('Processing cash less payment')
        return True

    def process_cash_on_delivery_payment(self):
        print('Processing cash on delivery payment')
        return True

    def post_payment_process(self):
        self.cart.status = Cart.CartStatusChoices.PAID
        self.cart.save()
        print('Payment processed successfully')

    def notify_user(self):
        print('User has been notified about payment')

