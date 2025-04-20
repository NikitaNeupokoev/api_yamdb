# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import signup, get_token, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/v1/auth/signup/', signup),
    path('api/v1/auth/token/', get_token),
    path('api/v1/', include(router.urls)),
]
