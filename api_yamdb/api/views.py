from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Comment, Review, Title, Category, Genre
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    CategorySerializer,
    GenreSerializer
)
from .viewsets import ListCreateDestroyViewSet


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    ViewSet для работы с категориями.

    Предоставляет операции "list", "create" и "destroy" для категорий.
    Доступ к созданию и удалению категорий разрешен только администраторам.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    ViewSet для работы с жанрами.

    Предоставляет операции "list", "create" и "destroy" для жанров.
    Доступ к созданию и удалению жанров разрешен только администраторам.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с произведениями.

    Предоставляет CRUD-операции для произведений.
    Доступ к созданию, обновлению и удалению произведений разрешен.
    только администраторам.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.

    Предоставляет CRUD-операции для отзывов к произведениям.
    Автоматически устанавливает автора и произведение при создании отзыва.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.

    Предоставляет CRUD-операции для комментариев к отзывам.
    Автоматически устанавливает автора и отзыв при создании комментария.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Comment.objects.filter(
            review=self.kwargs.get('review_id')
        )

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
