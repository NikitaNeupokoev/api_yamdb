from django.urls import include, path

from api.v1.users.views import signup, get_token

app_name = 'api'

urlpatterns = [
    path('v1', include('api.v1.reviews.urls')),
    path('v1/users/', include('api.v1.users.urls')),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
]
