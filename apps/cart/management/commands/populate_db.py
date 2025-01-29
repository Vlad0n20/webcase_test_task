from django.core.management.base import BaseCommand

from apps.cart.factories import CartFactory, CartProductFactory
from apps.product.factories import ProductFactory, CategoryFactory
from apps.product.models import Category, Product
from apps.user.factories import UserFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--products_count', type=int, help='Number of products to create')
        parser.add_argument('--categories_count', type=int, help='Number of products to create')
        parser.add_argument('--users_count', type=int, help='Number of users to create')
        parser.add_argument('--carts_count', type=int, help='Number of carts to create')

    def handle(self, *args, **options):
        products_count = options['products_count'] if options['products_count'] else 10
        categories_count = options['categories_count'] if options['categories_count'] else 3
        users_count = options['users_count'] if options['users_count'] else 3
        carts_count = options['carts_count'] if options['carts_count'] else 3
        for _ in range(categories_count):
            CategoryFactory.create()
        for _ in range(products_count):
            ProductFactory.create(category=Category.objects.order_by('?').first())

        for _ in range(users_count):
            UserFactory.create()

        for _ in range(carts_count):
            cart = CartFactory.create()
            for _ in range(5):
                CartProductFactory.create(cart=cart, product=Product.objects.order_by('?').first())

        self.stdout.write(self.style.SUCCESS('Successfully created users'))
