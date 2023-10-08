import datetime
import logging

import pytz
import requests
from django.conf import settings
from django.utils import timezone

from notification.models import Client, Message, Newsletter
from notification_service.celery import app

logger = logging.getLogger('main')


@app.task(bind=True, retry_backoff=True)
def send_message(self, message_id, client_id, newsletter_id):
    '''Задача на отправку сообщения.'''

    newsletter = Newsletter.objects.get(pk=newsletter_id)
    client = Client.objects.get(pk=client_id)
    client_now = datetime.datetime.now(pytz.timezone(client.time_zone))
    if newsletter.launch_date <= client_now <= newsletter.end_date:
        logger.info(f'Сообщение №{message_id} принято в работу.')
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {settings.TOKEN}',
        }
        body = {
            'id': message_id,
            'phone': int(client.phone_number),
            'text': newsletter.message_text,
        }
        try:
            logger.info(
                f'Запущен запрос на отправку сообщения №{message_id} '
                f'клиенту: {client.phone_number}.'
            )
            request = requests.post(
                url=settings.URL + str(message_id),
                json=body,
                headers=headers,
            )
        except requests.exceptions.RequestException as error:
            status = 'Service Unavailable'
            logger.warning(
                f'Ошибка при запросе на отправку сообщения №{message_id}: '
                f'{error}.'
            )
            raise self.retry(exc=error)
        else:
            if request.text:
                status = request.json()['message']
            else:
                status = 'Bad Request'
            logger.info(
                'Успешная обработка запроса на отправку сообщения №'
                f'{message_id} клиенту: {client.phone_number}.'
            )
        Message.objects.filter(pk=message_id).update(
            sending_date=timezone.now(),
            status=status,
        )
        logger.info(f'Сообщению №{message_id} присвоен статус: {status}.')
    else:
        delayed_start = int(
            (newsletter.launch_date - client_now).total_seconds()
        )
        logger.info(
            f'Перенос отправки сообщения №{message_id} на '
            f'{int(delayed_start/60)} минут.'
        )
        return self.retry(countdown=delayed_start)
