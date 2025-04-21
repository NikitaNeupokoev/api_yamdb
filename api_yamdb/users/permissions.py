from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """

    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь администратором.
        """
        return request.user.is_authenticated and request.user.is_admin
