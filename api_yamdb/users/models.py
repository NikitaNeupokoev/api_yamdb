from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.constants import MAX_LENGTH_ROLE


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        """Является ли пользователь администратором."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Является ли пользователь модератором."""
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
