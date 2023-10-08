from rest_framework import serializers

from notification.models import Client, Message, Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = (
            'id',
            'code',
            'tag',
            'launch_date',
            'message_text',
            'end_date',
        )

    def validate(self, data):
        if data['launch_date'] > data['end_date']:
            raise serializers.ValidationError(
                'Дата запуска не может быть позже даты окончания рассылки!'
            )
        return data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'code', 'tag', 'phone_number', 'time_zone')


class MessageSerializer(serializers.ModelSerializer):
    newsletter = NewsletterSerializer()
    client = ClientSerializer()

    class Meta:
        model = Message
        fields = ('id', 'sending_date', 'status', 'newsletter', 'client')
