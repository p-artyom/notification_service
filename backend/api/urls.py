from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from api.views import ClientViewSet, MessageViewSet, NewsletterViewSet

router = routers.DefaultRouter()
router.register('newsletters', NewsletterViewSet, basename='newsletters')
router.register('clients', ClientViewSet, basename='clients')
router.register('messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
        ),
        name='swagger-ui',
    ),
]
