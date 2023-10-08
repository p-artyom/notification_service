import logging

from django.db.models import Q, signals
from django.dispatch import receiver
from django.utils import timezone

from api.tasks import send_message
from notification.models import Client, Message, Newsletter

logger = logging.getLogger('main')


@receiver(signals.post_save, sender=Newsletter)
def creating_task(sender, instance, created, **kwargs):
    '''Обработка события сохранения данных в сущность `рассылка`.'''

    del sender, created, kwargs
    now = timezone.now()
    newsletter = Newsletter.objects.get(id=instance.id)
    if newsletter.launch_date <= now <= newsletter.end_date:
        logger.info(f'Рассылка №{instance.id} принята в работу.')
        delayed_start = 0
    elif newsletter.launch_date > now:
        delayed_start = int((newsletter.launch_date - now).total_seconds())
        logger.info(
            f'Перенос рассылки №{instance.id} на '
            f'{int(delayed_start/60)} минут.'
        )
    else:
        logger.info(f'Рассылка №{instance.id} просрочена.')
        return
    clients = Client.objects.filter(
        Q(code=newsletter.code) | Q(tag=newsletter.tag)
    )
    for client in clients:
        message, created = Message.objects.get_or_create(
            newsletter=newsletter,
            client=client,
        )
        if created:
            message.status = 'Created'
            message.save()
            logger.info(f'Сообщение №{message.id} создано.')
        send_message.apply_async(
            (message.id, client.id, newsletter.id),
            countdown=delayed_start,
            expires=instance.end_date,
        )
