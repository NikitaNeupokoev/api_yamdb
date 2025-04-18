from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from django.db.models import Avg
from django.utils import timezone

from reviews.models import Category, Genre, Title, Review, Comment, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),

    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'genre', 'category',)
        model = Title

    @staticmethod
    def get_rating(obj):
        """Подсчет среднего значения рейтинга"""
        #Не проверял пока просто скопировал переписал из model
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score is not None:
            return avg_score
        else:
            return 0.0

    @staticmethod
    def validate_year(values):
        """Метод для валидации значения year"""
        if values > timezone.now().year:
            raise ValidationError(
                {'year': 'год выпуска не может быть больше текущего'}
            )
        return values


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)
        model = Review

    # Не знаю как лучше проверять здесь или в perform_create во views.py
    # тут как бы лишний запрос к базе
    # def validate(self, data):
    #     title = get_object_or_404(
    #         Title,
    #         pk=self.context.get('view').kwargs['title_id']
    #     )
    #     author = self.context.get('request').user
    #     if (
    #         self.context.get('request').method == 'POST'
    #         and title.reviews.filter(author=author).exists()
    #     ):
    #         raise ValidationError(
    #             {'review': 'Вы уже писали отзыв для данного произведения'}
    #         )
    #     return data





class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date',)
        read_only_fields = ('review',)
        model = Comment


#TO DO Описать после создания кастомной модели юзера
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             'username', 'email', 'first_name',
#             'last_name', 'bio', 'role'
#         )
#         model = User
