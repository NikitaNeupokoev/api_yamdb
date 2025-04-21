from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleReadSerializer,ReviewSerializer,
                          CommentSerializer)

from reviews.models import Category, Genre, Title, Review, Comment, User
from .viewsets import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsAuthorOrStaff


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    list: Получить список всех категорий Права доступа: Доступно без токена

    create: Создать категорию. Права доступа: Администратор.
    Поле slug каждой категории должно быть уникальным.

    destroy: Удалить категорию. Права доступа: Администратор.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    list: Получить список всех жанров. Права доступа: Доступно без токена

    create: Добавить жанр. Права доступа: Администратор.
    Поле slug каждого жанра должно быть уникальным.

    destroy: Удалить жанр. Права доступа: Администратор.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """
    list: Получить список всех объектов. Права доступа: Доступно без токена

    retrieve: Информация о произведении Права доступа: Доступно без токена

    create: Добавить новое произведение. Права доступа: Администратор.
    Нельзя добавлять произведения, которые еще не вышли (год выпуска не может
    быть больше текущего). При добавлении нового произведения требуется
    указать уже существующие категорию и жанр.

    partial_update: Обновить информацию о произведении
    Права доступа: Администратор

    destroy: Удалить произведение. Права доступа: Администратор.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list') :
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    list: Получить список всех отзывов. Права доступа: Доступно без токена.

    retrieve: Получить отзыв по id для указанного произведения.
    Права доступа: Доступно без токена.

    create: Добавить новый отзыв. Пользователь может оставить только один отзыв
    на произведение. Права доступа: Аутентифицированные пользователи.

    partial_update: Частично обновить отзыв по id.
    Права доступа: Автор отзыва, модератор или администратор.

    destroy: Удалить отзыв по id
    Права доступа: Автор отзыва, модератор или администратор.
    """
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action == 'create':
             return (IsAuthenticated(),)
        elif self.action in ('partial_update', 'destroy'):
            return (IsAuthenticated(), IsAuthorOrStaff(),)
        else:
            return (AllowAny(),)


    def get_title(self):
        """
        Метод возвращает произведение по его id или ошибку 404 (Not Found)
        в случае его отсутствия
        """
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        author = self.request.user
        if (
            self.request.method == 'POST'
            and title.reviews.filter(author=author).exists()
        ):
            raise ValidationError(
                {'review': 'Вы уже писали отзыв для данного произведения'}
            )
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    list: Получить список всех комментариев к отзыву по id
    Права доступа: Доступно без токена.

    retrieve: Получить комментарий для отзыва по id.
    Права доступа: Доступно без токена.

    create: Добавить новый комментарий для отзыва.
    Права доступа: Аутентифицированные пользователи.

    partial_update: Частично обновить комментарий к отзыву по id.
    Права доступа: Автор комментария, модератор или администратор.

    destroy: Удалить комментарий к отзыву по id.
    Права доступа: Автор комментария, модератор или администратор.
    """
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action == 'create':
             return (IsAuthenticated(),)
        elif self.action in ('partial_update', 'destroy'):
            return (IsAuthenticated(), IsAuthorOrStaff(),)
        else:
            return (AllowAny(),)

    def get_review(self):
        """
        Метод возвращает отзыв по его id или ошибку 404 (Not Found)
        в случае его отсутствия
        """
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
