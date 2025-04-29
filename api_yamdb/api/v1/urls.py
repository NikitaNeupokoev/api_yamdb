from django.urls import include, path

from api.v1.users.views import signup, get_token

app_name = 'api'

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('', include('api.v1.reviews.urls')),
    path('users/', include('api.v1.users.urls')),
    path('auth/', include(auth_patterns)),
]
