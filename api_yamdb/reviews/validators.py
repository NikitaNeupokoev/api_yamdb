from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.constants import MIN_YEAR


def validate_year(values):
    """Валидации значения year."""
    current_year = timezone.now().year
    if MIN_YEAR > values:
        error_message = f'год выпуска не может быть меньше {MIN_YEAR}.'

    elif values > current_year:
        error_message = (f'год выпуска не может быть больше {current_year}.')

    else:
        return values

    raise ValidationError(error_message)
