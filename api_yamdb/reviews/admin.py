from django.contrib import admin

from .models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для модели Category."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административная панель для модели Genre."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Административная панель для модели Title."""

    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'category')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административная панель для модели Review."""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('text',)
    list_editable = ('text', 'author', 'score')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административная панель для модели Comment."""

    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date'
    )
    search_fields = ('text',)
    empty_value_display = '-пусто-'
