import pytz
from django.core.validators import RegexValidator

PHONE_REGEX = RegexValidator(
    regex=r'^7\d{10}$',
    message=(
        'Номер телефона должен быть в формате 7XXXXXXXXXX, '
        'где X - цифра от 0 до 9.'
    ),
)

TIME_ZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
