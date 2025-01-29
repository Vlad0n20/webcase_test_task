from rest_framework.viewsets import ModelViewSet

from abstract.mixins import MixedPermission


class CustomModelViewSet(MixedPermission, ModelViewSet):
    permission_classes_by_action = {}

