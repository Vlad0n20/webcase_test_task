from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from abstract.mixins import MixedPermission
from core.yasg import CustomSwaggerViewSetTag


class CustomModelViewSet(MixedPermission, ModelViewSet):
    permission_classes_by_action = {}
    swagger_schema = CustomSwaggerViewSetTag

    # def list(self, request, *args, **kwargs):
    #     try:
    #         return super().list(request, *args, **kwargs)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def create(self, request, *args, **kwargs):
    #     try:
    #         return super().create(request, *args, **kwargs)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         return super().retrieve(request, *args, **kwargs)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request, *args, **kwargs):
    #     try:
    #         return super().update(request, *args, **kwargs)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         return super().destroy(request, *args, **kwargs)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
