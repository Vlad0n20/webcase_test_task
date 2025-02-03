from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from abstract.viewset import CustomModelViewSet

from .models import Cart
from . import serializers
from .services.payment import PaymentProcessor


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

    @action(methods=['post'], detail=True)
    def payment(self, request, *args, **kwargs):
        serializer = serializers.CartPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.get_object()
        try:
            PaymentProcessor(
                cart=cart,
                payment_data=serializer.validated_data.get('payment_data')
            ).process_payment()
            cart.status = Cart.CartStatusChoices.PAID
            cart.save()
        except ValueError as e:
            cart.status = Cart.CartStatusChoices.INACTIVE
            cart.save()
            raise ValidationError(e)
        return Response({'status': 'Paid'})

