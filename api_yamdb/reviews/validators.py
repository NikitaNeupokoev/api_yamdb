from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.constants import MIN_YEAR


def validate_year(values):
    """Валидации значения year."""
    current_year = timezone.now().year

    if MIN_YEAR > values:
        raise ValidationError(
            f'Год выпуска не может быть меньше {MIN_YEAR}.'
        )

    if values > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше {current_year}.'
        )

    return values
