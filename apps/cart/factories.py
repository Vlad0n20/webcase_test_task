import factory.django

from apps.cart.models import Cart, CartProduct

class CartProductFactory(factory.django.DjangoModelFactory):
    quantity = factory.Faker('random_number', digits=2)
    product = factory.SubFactory('apps.product.factories.ProductFactory')

    class Meta:
        model = CartProduct

class CartFactory(factory.django.DjangoModelFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = CartProductFactory.create_batch(5)


    class Meta:
        model = Cart