from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение: только администратор или только чтение."""

    def has_permission(self, request, view):
        """Проверка прав доступа для запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrStaff(permissions.BasePermission):
    """Разрешение: автор или персонал."""

    def has_permission(self, request, view):
        """Проверка прав доступа для запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
