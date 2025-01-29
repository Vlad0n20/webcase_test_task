from rest_framework import serializers

from .models import Product, Category
from apps.user.serializers import UserListSerializer

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
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category_id']