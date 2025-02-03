from abstract.viewset import CustomModelViewSet

from .models import Product, Category
from . import serializers


class ProductViewSet(CustomModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProductCreateSerializer
        elif self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.ProductUpdateSerializer
        return super().get_serializer_class()




class CategoryViewSet(CustomModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CategoryCreateSerializer
        elif self.action == 'retrieve':
            return serializers.CategoryDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.CategoryUpdateSerializer
        return super().get_serializer_class()

