from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Review, Title
from .serializers import CommentSerializer, ReviewSerializer, TitleSerializer


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели Title (заглушка).

    Предоставляет операции только для чтения для произведений.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # TODO: Настроить права доступа
    permission_classes = [permissions.IsAdminUser]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.

    Предоставляет CRUD-операции для отзывов к произведениям.
    Автоматически устанавливает автора и произведение при создании отзыва.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_title(self):  # Добавим этот метод
        return get_object_or_404(Title, pk=self.kwargs['title_id'])


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
