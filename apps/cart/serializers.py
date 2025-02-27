from datetime import datetime

from rest_framework import serializers

from utils.fields import ChoicesField
from .models import Cart, CartProduct
from apps.user.serializers import UserListSerializer
from apps.product.serializers import ProductListSerializer, ProductDetailSerializer
from .services.cart import CartProcessor
from .services.payment import PaymentProcessor

class CartProductListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductListSerializer(instance.product).data
        return data

    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'quantity']

class CartProductDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductListSerializer(instance.product).data
        return data

    class Meta:
        model = CartProduct
        fields = ['id', 'quantity']

class CartListSerializer(serializers.ModelSerializer):
    delivery_type = ChoicesField(Cart.DeliveryTypeChoices)
    payment_type = ChoicesField(Cart.PaymentTypeChoices)

    def to_representation(self, instance):
        # стосовно переписування to_representation. В деякий випажках серіалізатор може мінятись
        # наприклад, запит робить адміністратор, тому він може бачити більше інформаціїй
        # у цьому випадку тут пожна поміняти серіалізатор на більш підходящий
        data = super().to_representation(instance)
        data['created_by'] = UserListSerializer(instance.created_by).data
        return data

    class Meta:
        model = Cart
        fields = ['id', 'created_by', 'total_price', 'delivery_type', 'payment_type']

class CartDetailSerializer(serializers.ModelSerializer):
    delivery_type = ChoicesField(Cart.DeliveryTypeChoices)
    payment_type = ChoicesField(Cart.PaymentTypeChoices)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = UserListSerializer(instance.created_by).data
        data['products'] = CartProductDetailSerializer(instance=instance.cartproduct_set.all(), many=True).data
        return data

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'created_by', 'delivery_type', 'payment_type']

class CartItemCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']

class CartCreateSerializer(serializers.ModelSerializer):
    products = CartItemCreateSerializer(many=True)
    discount_for_each_product = serializers.BooleanField(default=False)
    payment_data = serializers.JSONField(default=dict)
    delivery_data = serializers.JSONField(default=dict)

    def create(self, validated_data):
        products = validated_data.pop('products')
        cart = Cart.objects.create(**validated_data)
        products_list = []
        for product in products:
            products_list.append(CartProduct(cart=cart, **product))
        CartProduct.objects.bulk_create(products_list)
        processor = CartProcessor(cart)
        total_price = processor.calculate_total_price()
        cart.total_price = total_price
        cart.save()
        return cart

    class Meta:
        model = Cart
        fields = ['products', 'discount_for_each_product', 'delivery_type',
                  'delivery_address', 'payment_type', 'payment_data', 'delivery_data']

class CartUpdateUpdateSerializer(serializers.ModelSerializer):
    products = CartItemCreateSerializer(many=True)

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        products_list = []
        for product in products:
            products_list.append(CartProduct(cart=instance, **product))
        CartProduct.objects.bulk_create(products_list)
        processor = CartProcessor(instance)
        new_total_price = processor.calculate_total_price()
        instance.total_price = new_total_price
        instance.save()
        return instance

    class Meta:
        model = Cart
        fields = ['products', 'delivery_type', 'delivery_address', 'payment_type']

class CartPaymentSerializer(serializers.Serializer):
    payment_data = serializers.JSONField(default=dict)

    class Meta:
        model = Cart
        fields = ['payment_data']