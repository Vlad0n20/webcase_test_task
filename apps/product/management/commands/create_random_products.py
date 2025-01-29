from django.core.management.base import BaseCommand


from apps.product.factories import ProductFactory, CategoryFactory
from apps.product.models import Category


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--products_count', type=int, help='Number of products to create')
        parser.add_argument('--categories_count', type=int, help='Number of products to create')

    def handle(self, *args, **options):
        categories_count = options['categories_count'] if options['categories_count'] else 3
        for _ in range(categories_count):
            CategoryFactory.create()
        products_count = options['products_count'] if options['products_count'] else 10
        for _ in range(products_count):
            ProductFactory.create(category=Category.objects.order_by('?').first())
        self.stdout.write(self.style.SUCCESS('Successfully created {} users'.format(products_count)))
