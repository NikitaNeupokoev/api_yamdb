from django.urls import include, path

from api.v1.users.views import signup, get_token

app_name = 'api'

urlpatterns = [
    path('', include('api.v1.reviews.urls')),
    path('users/', include('api.v1.users.urls')),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='get_token'),
]
