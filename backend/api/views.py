import logging

from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.serializers import (
    ClientSerializer,
    MessageSerializer,
    NewsletterSerializer,
)
from notification.models import Client, Message, Newsletter

logger = logging.getLogger('main')


@extend_schema_view(
    list=extend_schema(summary='Получить список всех рассылок'),
    create=extend_schema(summary='Создать данные рассылки'),
    retrieve=extend_schema(summary='Получить данные рассылки'),
    update=extend_schema(summary='Обновить данные рассылки целиком'),
    partial_update=extend_schema(summary='Обновить данные рассылки частично'),
    destroy=extend_schema(summary='Удалить данные рассылки'),
    total_statistics=extend_schema(
        summary='Общая статистика по созданным рассылкам',
    ),
    detailed_statistics=extend_schema(
        summary='Детальная статистика по конкретной рассылке',
    ),
)
class NewsletterViewSet(CRUDAPIView):
    '''Рассылка.'''

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_create(self, serializer):
        newsletter = serializer.save()
        logger.info(f'Рассылка №{newsletter.id} создана.')

    def perform_update(self, serializer):
        newsletter = serializer.save()
        logger.info(f'Рассылка №{newsletter.id} обновлена.')

    def perform_destroy(self, instance):
        logger.info(f'Рассылка №{instance.id} удалена.')
        instance.delete()

    @action(detail=False, methods=['GET'])
    def total_statistics(self, request):
        '''Общая статистика по созданным рассылкам.'''
        del request
        newsletters = Newsletter.objects.all()
        response = []
        for newsletter in newsletters:
            statistics = {
                'newsletter': NewsletterSerializer(newsletter).data,
                'total messages': (
                    Message.objects.filter(newsletter=newsletter).count()
                ),
                'messages': list(
                    Message.objects.filter(newsletter=newsletter)
                    .values('status')
                    .annotate(total_with_this_status=Count('id'))
                ),
            }
            response.append(statistics)
        return Response(response)

    @action(detail=True, methods=['GET'])
    def detailed_statistics(self, request, pk=None):
        '''Детальная статистика по конкретной рассылке.'''
        del request
        newsletter = get_object_or_404(Newsletter, pk=pk)
        return Response(
            MessageSerializer(
                Message.objects.filter(newsletter=newsletter), many=True
            ).data
        )


@extend_schema_view(
    list=extend_schema(summary='Получить список всех клиентов'),
    create=extend_schema(summary='Создать данные клиента'),
    retrieve=extend_schema(summary='Получить данные клиента'),
    update=extend_schema(summary='Обновить данные клиента целиком'),
    partial_update=extend_schema(summary='Обновить данные клиента частично'),
    destroy=extend_schema(summary='Удалить данные клиента'),
)
class ClientViewSet(CRUDAPIView):
    '''Клиенты.'''

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        client = serializer.save()
        logger.info(f'Клиент №{client.id} создан.')

    def perform_update(self, serializer):
        client = serializer.save()
        logger.info(f'Клиент №{client.id} обновлен.')

    def perform_destroy(self, instance):
        logger.info(f'Клиент №{instance.id} удален.')
        instance.delete()


@extend_schema_view(
    list=extend_schema(summary='Получить список всех сообщений'),
    retrieve=extend_schema(summary='Получить данные сообщения'),
)
class MessageViewSet(ListRetrieveAPIView):
    '''Сообщения.'''

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
