from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from django.db.models import Avg

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
        slug_field='name',
        queryset=Genre.objects.all(),
        many=True
    )
    category = SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),

    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'genre', 'category',)
        model = Title

    def get_rating(self, obj):
        """Подсчет среднего значения рейтинга"""
        #Не проверял пока просто скопировал переписал из model
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score is not None:
            return avg_score
        else:
            return 0.0


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
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже писали отзыв для данного произведения'
            )
        ]


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
