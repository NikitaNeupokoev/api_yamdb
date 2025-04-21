from django.contrib.auth import get_user_model

from rest_framework import serializers
from django.db.models import Avg
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Предоставляет информацию о категории, включая:
        - name: Название категории.
        - slug: Идентификатор категории.
    """
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.

    Предоставляет информацию о жанре, включая:
        - name: Название жанра.
        - slug: Идентификатор жанра.
    """
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.

    Предоставляет информацию о произведении, включая:
        - id: ID произведения.
        - name: Название произведения.
        - year: Год создания.
        - rating: Рейтинг произведения (только для чтения).
        - genre: Список жанров (только для SlugRelatedField).
        - category: Категория произведения (только для SlugRelatedField).

    Notes:
        1)  Поле `rating` вычисляется динамически и доступно только для чтения.
        2)  Поля `genre` и `category` используют `SlugRelatedField` для
            отображения и выбора жанров и категорий по их названиям (slug).
    """
    rating = serializers.SerializerMethodField()
    genre = SlugRelatedField(
        slug_field='name',
        queryset=Genre.objects.all(),
        many=True
    )
    category = SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),

    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'genre', 'category',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.

    Предоставляет информацию об отзыве, включая:
        - id: ID отзыва.
        - title: Произведение, к которому относится
        .отзыв (только для чтения).
        - text: Текст отзыва.
        - author: Автор отзыва (username, только для чтения).
        - score: Оценка произведения.
        - pub_date: Дата публикации отзыва.

    Notes:
        1) Поле 'author' отображается как username автора (только для чтения).
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Предоставляет информацию о комментарии, включая:
        - id: ID комментария.
        - review: Отзыв, к которому относится комментарий.
        (только для чтения).
        - text: Текст комментария.
        - author: Автор комментария.
        (username, только для чтения).
        - pub_date: Дата публикации комментария.

    Notes:
        1)  Поле `author` использует `SlugRelatedField`.
        для отображения автора по username.
        и является полем только для чтения.
        2)  Поле `review` является полем только для чтения.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)
        read_only_fields = ('review',)
