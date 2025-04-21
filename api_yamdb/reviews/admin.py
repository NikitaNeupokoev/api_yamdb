from django.contrib import admin

from .models import (
    Category,
    CustomUser,
    Comment,
    Genre,
    Review,
    Title
)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
    list_editable = ('text', 'author', 'score')


admin.site.register(CustomUser)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment)
