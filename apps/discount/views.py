from abstract.viewset import CustomModelViewSet

from .models import Discount
from . import serializers


class DiscountViewSet(CustomModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountDetailSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.DiscountCreateSerializer
        return super().get_serializer_class()

