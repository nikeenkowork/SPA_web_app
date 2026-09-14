from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Разрешение только для пользователей группы Модераторы."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )

class IsOwner(BasePermission):
    """Разрешение только для владельца объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user