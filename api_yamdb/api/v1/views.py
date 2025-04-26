from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.filters import TitleFilter
from api.v1.permissions import IsAdminOrReadOnly, IsAuthorOrStaff
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleCreateUpdateSerializer,
)
from api.v1.viewsets import ListCreateDestroyViewSet, ViewSetWithoutUpdate
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    ViewSet для модели Category.

    Предоставляет операции list, create, destroy для категорий.

    Права доступа:
        - list: Доступно без токена.
        - create: Администратор. Поле slug каждой категории.
        должно быть уникальным.
        - destroy: Администратор.
    """

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    ViewSet для модели Genre.

    Предоставляет операции list, create, destroy для жанров.

    Права доступа:
        - list: Доступно без токена.
        - create: Администратор. Поле slug каждого жанра.
        должно быть уникальным.
        - destroy: Администратор.
    """

    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(ViewSetWithoutUpdate):
    """
    ViewSet для модели Title.

    Предоставляет операции list, retrieve, create, partial_update, destroy.
    для произведений.

    Права доступа:
        - list: Доступно без токена.
        - retrieve: Доступно без токена.
        - create:
    """

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleCreateUpdateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.

        Для операций retrieve и list используется TitleReadSerializer,
        для остальных - TitleCreateUpdateSerializer.
        """
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleCreateUpdateSerializer


class ReviewViewSet(ViewSetWithoutUpdate):
    """
    ViewSet для модели Review.

    Предоставляет операции list, retrieve, create, partial_update, destroy.
    для отзывов.

    Права доступа:
        - list: Доступно без токена.
        - retrieve: Доступно без токена.
        - create: Аутентифицированные пользователи.
        (только один отзыв на произведение).
        - partial_update: Автор отзыва, модератор или администратор.
        - destroy: Автор отзыва, модератор или администратор.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaff,)

    def get_title(self):
        """Возвращает произведение по его ID или вызывает 404."""
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Возвращает queryset отзывов для данного произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает новый отзыв."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ViewSetWithoutUpdate):
    """
    ViewSet для модели Comment.

    Предоставляет операции list, retrieve, create, partial_update, destroy.
    для комментариев.

    Права доступа:
        - list: Доступно без токена.
        - retrieve: Доступно без токена.
        - create: Аутентифицированные пользователи.
        - partial_update: Автор комментария, модератор или администратор.
        - destroy: Автор комментария, модератор или администратор.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaff,)

    def get_review(self):
        """Возвращает отзыв по его ID или вызывает 404."""
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Возвращает queryset комментариев для данного отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
