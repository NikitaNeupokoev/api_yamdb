from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_LENGHT = 150


#TO DO необходимо будет переписать через AbstractBaseUser
class CustomUser(AbstractUser):
    """Пользовательсчкая моедль User"""
    pass


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(verbose_name='Название категории',
                            max_length=MAX_LENGHT)
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(verbose_name='Название жанра',
                            max_length=MAX_LENGHT)
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=MAX_LENGHT
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания'
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', null=True
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_for_title'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'комменатрий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
