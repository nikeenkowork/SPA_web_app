from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Разрешение только для пользователей группы Модераторы."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )
