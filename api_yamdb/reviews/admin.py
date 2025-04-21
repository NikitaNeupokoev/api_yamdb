from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Review, Category, Genre, Title, Comment, CustomUser


admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(CustomUser, UserAdmin)