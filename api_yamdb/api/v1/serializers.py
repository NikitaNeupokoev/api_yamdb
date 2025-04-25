from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)
from api_yamdb.constants import MIN_YEAR


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

    rating = serializers.FloatField(read_only=True)
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


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
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
        current_year = timezone.now().year
        if MIN_YEAR > values:
            error_message = f'год выпуска не может быть меньше {MIN_YEAR}.'

        elif values > current_year:
            error_message = ('год выпуска не может '
                             f'быть больше {current_year}.')

        else:
            return values

        raise ValidationError({'year': error_message})


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

    def validate(self, data):
        """
        Проверка наличия существующего отзыва от пользователя.
        """
        title = get_object_or_404(
            Title,
            pk=self.context.get('view').kwargs['title_id']
        )
        author = self.context.get('request').user
        if (
            self.context.get('request').method == 'POST'
            and title.reviews.filter(author=author).exists()
        ):
            raise ValidationError(
                {'review': 'Вы уже писали отзыв для данного произведения'}
            )
        return data


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
