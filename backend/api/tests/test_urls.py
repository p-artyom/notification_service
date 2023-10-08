from http import HTTPStatus

from django.test import TestCase
from mixer.backend.django import mixer


class UrlsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.newsletter = mixer.blend('notification.Newsletter')
        cls.client = mixer.blend('notification.Client')

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.urls = {
            'clients': '/api/clients/',
            'client': f'/api/clients/{cls.client.id}/',
            'unknown_client': '/api/clients/99/',
            'newsletters': '/api/newsletters/',
            'newsletter': f'/api/newsletters/{cls.newsletter.id}/',
            'unknown_newsletter': '/api/newsletters/99/',
            'detailed_statistics': f'/api/newsletters/{cls.newsletter.id}/detailed_statistics/',
            'unknown_detailed_statistics': '/api/newsletters/99/detailed_statistics/',
            'total_statistics': '/api/newsletters/total_statistics/',
        }

    def test_http_statuses_get_request(self) -> None:
        '''URL-адрес возвращает соответствующий статус при GET запросах.'''
        urls_statuses_users = (
            (self.urls.get('clients'), HTTPStatus.OK, self.client),
            (self.urls.get('client'), HTTPStatus.OK, self.client),
            (
                self.urls.get('unknown_client'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (self.urls.get('newsletters'), HTTPStatus.OK, self.client),
            (self.urls.get('newsletter'), HTTPStatus.OK, self.client),
            (
                self.urls.get('unknown_newsletter'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (
                self.urls.get('detailed_statistics'),
                HTTPStatus.OK,
                self.client,
            ),
            (self.urls.get('total_statistics'), HTTPStatus.OK, self.client),
            (
                self.urls.get('unknown_detailed_statistics'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
        )
        for url, status, user in urls_statuses_users:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(user.get(url).status_code, status)

    def test_http_statuses_post_request(self) -> None:
        '''URL-адрес возвращает соответствующий статус при POST запросах.'''
        urls_statuses_users_data = (
            (
                self.urls.get('clients'),
                HTTPStatus.CREATED,
                self.client,
                {
                    'code': 'str',
                    'tag': 'string',
                    'phone_number': '75562691500',
                    'time_zone': 'Asia/Irkutsk',
                },
            ),
            (
                self.urls.get('newsletters'),
                HTTPStatus.CREATED,
                self.client,
                {
                    'code': 'str',
                    'tag': 'string',
                    'launch_date': '2023-10-06T10:30:00.595Z',
                    'message_text': 'string',
                    'end_date': '2023-10-08T10:30:00.595Z',
                },
            ),
            (
                self.urls.get('clients'),
                HTTPStatus.BAD_REQUEST,
                self.client,
                {},
            ),
            (
                self.urls.get('newsletters'),
                HTTPStatus.BAD_REQUEST,
                self.client,
                {},
            ),
        )
        for url, status, user, data in urls_statuses_users_data:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(
                    user.post(url, data=data, format='json').status_code,
                    status,
                )

    def test_http_statuses_patch_request(self) -> None:
        '''URL-адрес возвращает соответствующий статус при PATCH запросах.'''
        urls_statuses_users_data = (
            (
                self.urls.get('client'),
                HTTPStatus.OK,
                self.client,
                {
                    'code': 'new',
                    'tag': 'new_string',
                    'phone_number': '75562691500',
                },
            ),
            (
                self.urls.get('client'),
                HTTPStatus.BAD_REQUEST,
                self.client,
                {
                    'code': 'new_str',
                    'taggg': 'new_string',
                    'phone_numberrr': '75562691500',
                },
            ),
            (
                self.urls.get('newsletter'),
                HTTPStatus.OK,
                self.client,
                {
                    'code': 'new',
                    'launch_date': '2023-10-06T10:30:00.595Z',
                    'message_text': 'new_string',
                    'end_date': '2023-10-08T10:30:00.595Z',
                },
            ),
            (
                self.urls.get('newsletter'),
                HTTPStatus.BAD_REQUEST,
                self.client,
                {
                    'code': 'new_str',
                    'launch_date': '2023-10-06T10:30:00.595Z',
                    'message_texttt': 'new_string',
                    'end_date': '2023-10-08T10:30:00.595Z',
                },
            ),
        )
        for url, status, user, data in urls_statuses_users_data:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(
                    user.patch(
                        url,
                        data=data,
                        format='json',
                        content_type='application/json',
                    ).status_code,
                    status,
                )

    def test_http_statuses_delete_request(self) -> None:
        '''URL-адрес возвращает соответствующий статус при DELETE запросах.'''
        urls_statuses_users = (
            (
                self.urls.get('client'),
                HTTPStatus.NO_CONTENT,
                self.client,
            ),
            (
                self.urls.get('client'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (
                self.urls.get('unknown_client'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (
                self.urls.get('newsletter'),
                HTTPStatus.NO_CONTENT,
                self.client,
            ),
            (
                self.urls.get('newsletter'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (
                self.urls.get('unknown_newsletter'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
        )
        for url, status, user in urls_statuses_users:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(
                    user.delete(url).status_code,
                    status,
                )
