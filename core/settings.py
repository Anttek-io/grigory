"""
Django settings for grigory project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()


def getenv(key, default=None):
    value = os.getenv(key, default)
    if value == '':
        return default
    if value == 'True':
        return True
    if value == 'False':
        return False
    return value


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY', 'django-insecure-0@=b%$ru-1i&(sc@thp8r&h$4c!6%y#qr^v=wcybcf)u7-=a*&')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DJANGO_DEBUG', True)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]

EXTRA_ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', None)

if EXTRA_ALLOWED_HOSTS:
    assert isinstance(EXTRA_ALLOWED_HOSTS.split(','), list)
    ALLOWED_HOSTS.extend(EXTRA_ALLOWED_HOSTS.split(','))

DJANGO_BASE_PATH = getenv('DJANGO_BASE_PATH', '')

if not DJANGO_BASE_PATH.endswith('/'):
    DJANGO_BASE_PATH += '/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'ms_auth_router',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',

    # Local apps
    'authentication',
    'app',
]

MIDDLEWARE = [
    'core.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3', conn_max_age=600)
}

DATABASE_ROUTERS = [
    'ms_auth_router.routers.DefaultRouter',
]

ROUTE_APP_LABELS = ('authentication', )

AUTH_DB = 'default'

if auth_db := os.getenv('AUTH_DB_URL'):
    AUTH_DB = 'auth_db'
    DATABASES['auth_db'] = dj_database_url.parse(auth_db)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = getenv('DJANGO_LANGUAGE_CODE', 'en')

TIME_ZONE = getenv('DJANGO_TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [

]

# Media files

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redis settings

REDIS_URL = getenv('REDIS_URL')

BROKER_URL = f'{REDIS_URL}/0'

# Celery settings

CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Channels settings

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# Django REST Framework settings

REST_AUTH_TOKEN_MODEL = 'authentication.Token'

REST_AUTH_TOKEN_TTL = getenv('DJANGO_REST_AUTH_TOKEN_TTL', 60 * 60 * 24)

REST_AUTH_TOKEN_CREATOR = 'authentication.utils.create_token'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'authentication.utils.ExpiringTokenAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.api.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

REST_EXPOSE_AUTH_API = getenv('DJANGO_REST_EXPOSE_AUTH_API', True)
