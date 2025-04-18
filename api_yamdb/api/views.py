from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer)

from reviews.models import Category, Genre, Title, Review, Comment, User
from .viewsets import ListCreateDestroyViewSet


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
    # permission_classes = (IsAdminOrReadOnly,)


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
    # permission_classes = (IsAdminOrReadOnly,)


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
    # permission_classes = (IsAdminOrReadOnly,)


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
    # permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

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
        if (
            self.request.method == 'POST'
            and title.reviews.filter(author=self.request.user).exists()
        ):
            raise ValidationError(
                {'review': 'Вы уже писали отзыв для данного произведения'}
            )
        serializer.save(author=self.request.user, title=title)


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
    # permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


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
