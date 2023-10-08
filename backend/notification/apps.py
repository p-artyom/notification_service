from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'notification'
    verbose_name = 'уведомление'

    def ready(self):
        from api import signals
