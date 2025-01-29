import factory.django

from .models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    description = factory.Faker('text')
    price = factory.Faker('random_number', digits=2)
    category = factory.SubFactory(CategoryFactory)


    class Meta:
        model = Product