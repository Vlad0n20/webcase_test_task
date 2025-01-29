from abstract.viewset import CustomModelViewSet

from .models import Cart
from . import serializers


class CartViewSet(CustomModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CartCreateSerializer
        elif self.action == 'retrieve':
            return serializers.CartDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.CartUpdateUpdateSerializer
        return super().get_serializer_class()

