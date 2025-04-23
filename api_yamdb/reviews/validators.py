from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.constants import MIN_YEAR


def validate_year(values):
    """Валидации значения year."""
    if MIN_YEAR > values > timezone.now().year:
        raise ValidationError(
            'год выпуска не может быть больше текущего'
        )
