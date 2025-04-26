from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import signup, get_token, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', get_token),
    path('', include(router.urls)),
]
