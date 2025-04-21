import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User
)

MODEL_CSV = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

#Не рабоает, нужно првить (загружает только User, Category, Genre)
class Command(BaseCommand):
    """Команда для загрузка данных из csv в model """

    help = 'Загрузка данных из csv в model'

    def handle(self, *args, **kwargs):
        for model, scv_file in MODEL_CSV.items():
            with open(
                    f'{settings.BASE_DIR}/static/data/{scv_file}', 'r',
                    encoding='utf-8'
            ) as file:
                self.stdout.write(f'Открыт: {scv_file}')
                reader = csv.DictReader(file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('БД обновлена'))
