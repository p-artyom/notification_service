import datetime

from django.test import TestCase
from mixer.backend.django import mixer

from notification.models import Message, Newsletter


class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.year = datetime.datetime.now().year
        cls.data = {
            'launch_date': f'{cls.year}-01-01T00:00:01.595Z',
            'end_date': f'{cls.year+1}-12-31T23:59:59.595Z',
            'late_now_time': f'{cls.year-2}-01-01T00:00:01.595Z',
            'late_end_date': f'{cls.year-1}-12-31T23:59:59.595Z',
            'code': '900',
            'tag': 'str',
            'phone_number': '75562691500',
            'time_zone': 'Asia/Irkutsk',
        }

    def test_newsletter_creates_message(self) -> None:
        '''Рассылка работает корректно.

        После создания новой рассылки, если текущее время больше времени
        начала и меньше времени окончания - должны быть выбраны из справочника
        все клиенты, которые подходят под значения фильтра, указанного в этой
        рассылке и запущена отправка для всех этих клиентов.
        '''
        self.assertEqual(
            Newsletter.objects.count(),
            0,
        )
        self.assertEqual(
            Message.objects.count(),
            0,
        )
        self.client = mixer.blend(
            'notification.Client',
            code=self.data['code'],
            tag=self.data['tag'],
            phone_number=self.data['phone_number'],
            time_zone=self.data['time_zone'],
        )
        self.newsletter = mixer.blend(
            'notification.Newsletter',
            launch_date=self.data['launch_date'],
            code=self.data['code'],
            tag=self.data['tag'],
            end_date=self.data['end_date'],
        )
        self.assertEqual(
            Newsletter.objects.count(),
            1,
        )
        self.assertEqual(
            Message.objects.count(),
            1,
        )

    def test_newsletter_no_creates_message(self) -> None:
        '''Просроченная рассылка работает корректно.

        Если создаётся просроченная рассылка, то объект в сущности
        `сообщение` не должен появиться.
        '''
        self.assertEqual(
            Newsletter.objects.count(),
            0,
        )
        self.assertEqual(
            Message.objects.count(),
            0,
        )
        self.client = mixer.blend(
            'notification.Client',
            code=self.data['code'],
            tag=self.data['tag'],
        )
        self.newsletter = mixer.blend(
            'notification.Newsletter',
            launch_date=self.data['late_now_time'],
            code=self.data['code'],
            tag=self.data['tag'],
            end_date=self.data['late_end_date'],
        )
        self.assertEqual(
            Newsletter.objects.count(),
            1,
        )
        self.assertEqual(
            Message.objects.count(),
            1,
        )
