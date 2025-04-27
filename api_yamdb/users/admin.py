from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Административная панель для модели User."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    search_fields = ('username',)
    empty_value_display = '-пусто-'
