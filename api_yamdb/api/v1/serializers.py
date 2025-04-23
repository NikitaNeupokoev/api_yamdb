from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""

    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'year',
            'rating',
            'genre',
            'category',
        )
        model = Title

    @staticmethod
    def get_rating(obj):
        """Подсчет среднего значения рейтинга"""
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score is not None:
            return avg_score
        else:
            return None


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/изменения произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'year',
            'genre',
            'category',
        )
        model = Title

    @staticmethod
    def validate_year(values):
        """Метод для валидации значения year"""
        if values > timezone.now().year:
            raise ValidationError(
                {'year': 'год выпуска не может быть больше текущего'}
            )
        return values


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'id',
            'review',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('review',)
        model = Comment
