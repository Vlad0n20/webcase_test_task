from datetime import datetime

from rest_framework import serializers

from utils.fields import ChoicesField
from .models import Cart, CartProduct
from apps.user.serializers import UserListSerializer
from apps.product.serializers import ProductListSerializer, ProductDetailSerializer
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
        data['product'] = ProductDetailSerializer(instance.product).data
        return data

    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'quantity']

class CartListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = UserListSerializer(instance.created_by).data
        return data

    class Meta:
        model = Cart
        fields = ['id', 'created_by']

class CartDetailSerializer(serializers.ModelSerializer):
    products = CartProductDetailSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = UserListSerializer(instance.created_by).data
        data['products'] = CartProductDetailSerializer(instance=instance.products.all(), many=True).data
        return data

    class Meta:
        model = Cart
        fields = ['id', 'products', 'total_price', 'created_by']

class CartItemCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']

class CartCreateSerializer(serializers.ModelSerializer):
    products = CartItemCreateSerializer(many=True)
    discount_for_each_product = serializers.BooleanField(default=False)
    delivery_type = ChoicesField(Cart.DeliveryTypeChoices)
    payment_type = ChoicesField(Cart.PaymentTypeChoices)
    payment_data = serializers.JSONField(default=dict)
    delivery_data = serializers.JSONField(default=dict)

    def create(self, validated_data):
        products = validated_data.pop('products')
        cart = Cart.objects.create(**validated_data)
        products_list = []
        for product in products:
            products_list.append(CartProduct(cart=cart, **product))
        CartProduct.objects.bulk_create(products_list)
        cart.calculate_total_price(
            discount_for_each_product=validated_data.get('discount_for_each_product'),
        )
        try:
            PaymentProcessor(cart=cart, payment_data=validated_data.get('payment_data')).process_payment()
        except ValueError as e:
            cart.status = Cart.CartStatusChoices.INACTIVE
            cart.save()
            raise serializers.ValidationError(e)
        return cart

    class Meta:
        model = Cart
        fields = ['products', 'discount_for_each_product', 'delivery_type',
                  'delivery_address', 'payment_type', 'payment_data', 'delivery_data']

class CartUpdateUpdateSerializer(serializers.ModelSerializer):
    products = CartItemCreateSerializer(many=True)
    discount_for_each_product = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        CartProduct.objects.filter(cart=instance).delete()
        products_list = []
        for product in products:
            products_list.append(CartProduct(cart=instance, **product))
        CartProduct.objects.bulk_create(products_list)
        instance.calculate_total_price(
            discount_for_each_product=validated_data.get('discount_for_each_product'),
        )
        return instance

    class Meta:
        model = Cart
        fields = ['products', 'discount_for_each_product']