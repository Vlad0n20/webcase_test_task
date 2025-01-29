class MixedPermission:
    """Mixin permissions for action"""

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except (KeyError, AttributeError):
            return [permission() for permission in self.permission_classes]
