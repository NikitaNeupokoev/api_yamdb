from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Category,
    Comment,
    CustomUser,
    Genre,
    Review,
    Title
)


class ReviewAdmin(admin.ModelAdmin):
    """Административная панель для модели Review."""

    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_editable = ('text', 'author', 'score')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment)
