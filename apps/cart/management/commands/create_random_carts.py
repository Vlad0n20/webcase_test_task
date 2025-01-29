from django.core.management.base import BaseCommand


from apps.cart.factories import CartFactory, CartProductFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--carts_count', type=int, help='Number of carts to create')

    def handle(self, *args, **options):
        carts_count = options['carts_count'] if options['carts_count'] else 3
        for _ in range(carts_count):
            cart = CartFactory.create()
            for _ in range(5):
                CartProductFactory.create(cart=cart)
        self.stdout.write(self.style.SUCCESS('Successfully created {} users'.format(carts_count)))
