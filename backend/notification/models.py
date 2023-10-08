from django.db import models

from core.models import DefaultModel
from core.utils import cut_string
from core.validators import PHONE_REGEX, TIME_ZONES


class Newsletter(DefaultModel):
    '''Сущность `рассылка`.'''

    launch_date = models.DateTimeField('дата и время запуска рассылки')
    message_text = models.TextField('текст сообщения для доставки клиенту')
    end_date = models.DateTimeField('дата и время окончания рассылки')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['pk']

    def __str__(self) -> str:
        return cut_string(f'Рассылка с {self.launch_date} по {self.end_date}')


class Client(DefaultModel):
    '''Сущность `клиент`.'''

    phone_number = models.CharField(
        'номер телефона',
        max_length=11,
        unique=True,
        validators=[PHONE_REGEX],
    )
    time_zone = models.CharField(
        'часовой пояс', max_length=200, choices=TIME_ZONES, default='UTC'
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['pk']

    def __str__(self) -> str:
        return cut_string(f'Клиент {self.phone_number}')


class Message(models.Model):
    '''Сущность `сообщение`.'''

    sending_date = models.DateTimeField(
        'дата и время отправки', null=True, blank=True
    )
    status = models.CharField(
        'статус отправки', max_length=200, null=True, blank=True
    )
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        verbose_name='рассылка',
        related_name='newsletter',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='клиент',
        related_name='client',
    )

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['pk']

    def __str__(self) -> str:
        return cut_string(
            f'{self.newsletter} отправлена на {self.client.phone_number}'
        )
