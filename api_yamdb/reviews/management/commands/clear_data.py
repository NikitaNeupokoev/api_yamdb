from django.core.management.base import BaseCommand
from reviews.models import (
    User,
    Category,
    Genre,
    Title,
    Review,
    Comment
)


class Command(BaseCommand):
    help = 'Очистка таблиц базы данных'

    def handle(self, *args, **options):
        User.objects.all().delete()
        Category.objects.all().delete()
        Genre.objects.all().delete()
        Title.objects.all().delete()
        Review.objects.all().delete()
        Comment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все таблицы очищены.'))
