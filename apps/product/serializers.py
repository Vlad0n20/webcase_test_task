from rest_framework import serializers

from .models import Product, Category
from apps.user.serializers import UserListSerializer
from ..cart.models import CartProduct


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = UserListSerializer(instance.created_by).data
        data['updated_by'] = UserListSerializer(instance.updated_by).data
        return data

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_on', 'updated_on', 'created_by', 'updated_by']

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryListSerializer(instance.category).data
        return data

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category']

class ProductDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryListSerializer(instance.category).data
        data['created_by'] = UserListSerializer(instance.created_by).data
        data['updated_by'] = UserListSerializer(instance.updated_by).data
        return data

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'created_on', 'updated_on', 'created_by', 'updated_by']

class ProductCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category_id']

class ProductUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'general_discount' in validated_data:
            active_carts = instance.carts.filter(status='created').values_list('id', flat=True)
            CartProduct.objects.filter(cart_id__in=active_carts, product=instance).update(discount=instance.general_discount)
        return instance
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category_id']