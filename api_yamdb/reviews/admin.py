from django.contrib import admin

from .models import Reviews, Categories, Genres, Titles, Comments

admin.site.register(Reviews)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
admin.site.register(Comments)
