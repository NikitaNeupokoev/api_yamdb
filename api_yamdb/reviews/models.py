from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.constants import (
    CHAR_FIELD_MAX_LENGHT,
    MIN_VALUE_SCORE,
    MAX_VALUE_SCORE,
    MAX_TEXT_LIGHT
)
from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        verbose_name='Название категории',
        max_length=CHAR_FIELD_MAX_LENGHT
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        verbose_name='Название жанра',
        max_length=CHAR_FIELD_MAX_LENGHT
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=CHAR_FIELD_MAX_LENGHT
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(MIN_VALUE_SCORE),
            MaxValueValidator(MAX_VALUE_SCORE),
        ),
        error_messages={
            'max_value': f'Оценка не должна превышать {MAX_VALUE_SCORE}.',
            'min_value': f'Оценка не должна быть меньше {MIN_VALUE_SCORE}.'
        }
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_for_title'
            )
        ]
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:100]


class Comment(models.Model):
    """Модель Комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:MAX_TEXT_LIGHT]
