from django.contrib import admin

from .models import Review, Category, Genre, Title, Comment

admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment)
