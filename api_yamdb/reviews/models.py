from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


User = get_user_model()

# Константа максимальное кол-во символов
MAX_LENGHT = 150


class Category(models.Model):
    """
    Модель категории произведения.
    """
    name = models.CharField(
        verbose_name='Название категории',
        max_length=MAX_LENGHT
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель жанра произведения.
    """
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=MAX_LENGHT
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
    """
    Модель произведения.
    """
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=MAX_LENGHT
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания'
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

    def update_rating(self):
        """
        Пересчитывает рейтинг произведения на основе отзывов.
        """
        avg_score = self.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score is not None:
            self.rating = avg_score
        else:
            self.rating = 0.0
        self.save()


class Review(models.Model):
    """
    Модель Отзыва.
    """
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
    )  # TODO:  После настройки User, заменить на ForeignKey
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']  # Отзывы сортируются от новых к старым

    def __str__(self):
        return self.text[:100]


class Comment(models.Model):
    """
    Модель Комментария.
    """
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
    )  # TODO:  После настройки User, заменить на ForeignKey
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:50]
