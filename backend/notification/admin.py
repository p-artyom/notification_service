from django.contrib import admin

from core.admin import BaseAdmin
from notification.models import Client, Message, Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(BaseAdmin):
    list_display = (
        'pk',
        'code',
        'tag',
        'launch_date',
        'message_text',
        'end_date',
    )
    list_filter = ('launch_date', 'end_date')
    search_fields = ('pk',)


@admin.register(Client)
class ClientAdmin(BaseAdmin):
    list_display = (
        'pk',
        'code',
        'tag',
        'phone_number',
        'time_zone',
    )
    list_filter = ('time_zone',)
    search_fields = ('phone_number',)


@admin.register(Message)
class MessageAdmin(BaseAdmin):
    list_display = (
        'pk',
        'sending_date',
        'status',
        'newsletter',
        'client',
    )
    list_filter = ('sending_date',)
    search_fields = ('pk',)
