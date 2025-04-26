from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('reviews/', include('api.v1.reviews.urls')),
    path('users/', include('api.v1.users.urls')),
]
