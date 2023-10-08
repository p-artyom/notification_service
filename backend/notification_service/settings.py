import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

DOTENV_PATH = BASE_DIR.parent / '.env'

if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')

CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379'
)

SECRET_KEY = os.getenv('SECRET_KEY', 'some-test-key-not-good-for-prod')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1 localhost').split(' ')

URL = os.getenv('URL', 'https://some-url/')

TOKEN = os.getenv('TOKEN', 'some-token')

# fmt: off
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api.apps.ApiConfig',
    'core.apps.CoreConfig',
    'notification.apps.NotificationConfig',

    'rest_framework',
    'drf_spectacular',
]
# fmt: on

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notification_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'notification_service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'django_password'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', 5432),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'collected_static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

STR_LENGTH_WHEN_PRINTING_MODEL = 50

SPECTACULAR_SETTINGS = {
    'TITLE': 'Список эндпоинтов API',
    'DESCRIPTION': 'Документация сервиса управления рассылками',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'CONTACT': {
        'email': 'artem38skull@yandex.ru',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s; %(levelname)-8s; %(message)s',
        },
    },
    'handlers': {
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'main.log',
            'level': 'INFO',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 4,
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['rotating_file'],
            'level': 'INFO',
        },
    },
}
