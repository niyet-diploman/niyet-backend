from datetime import timedelta

import environ
import git

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import sys
import dj_database_url


ROOT_DIR = environ.Path(
    __file__) - 2  # (monitoring_core/config/settings.py - 2 = monitoring_core/)

# Load operating system environment variables and then prepare to use them
env = environ.Env()

env_file = str(ROOT_DIR.path('.env'))
env.read_env(env_file)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, 'app')

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # grappelli must be before contrib admin, but its third party app
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_json_widget',
    'reversion',
    'reversion_compare',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'django_object_actions',
    'corsheaders',
    'app.users',
    'app.donations',
    'app.utility',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 10,
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=100),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=100),
}

AUTH_USER_MODEL = 'users.MyUser'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

gettext = lambda s: s

LANGUAGES = [
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
    ('kk', gettext('Kazakh')),
]

LOCALE_NAME = 'ru'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(ROOT_DIR, 'files')
MEDIA_URL = '/files/'

STATIC_ROOT = os.path.join(ROOT_DIR, '/static')
STATICFILES_DIRS = (os.path.join(APP_DIR, 'static'),)
STATIC_URL = '/static/'

CODE_EXPIRATION_TIME = 10  # 10 minutes

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
FROM_EMAIL = 'Niyet Team <niyet@gmail.com>'

EMAIL_CONFIG = env.email_url('EMAIL_URL')

vars().update(EMAIL_CONFIG)

GRAPPELLI_ADMIN_TITLE = 'Niyet - v2.0.0'

WS_REDIS_HOST = env.str('WS_REDIS_HOST')
WS_REDIS_PORT = env.str('WS_REDIS_PORT')

ENABLE_SWAGGER_ENDPOINT = True

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic',
        },
        'api_key': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },

    }
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# SITE_URL = 'http://localhost:18000'


RESET_PASSWORD_EXPIRE = 600
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

PAYBOX_SECRET_KEY = "ddbVlmwm9UexzuuR"
PAYBOX_MERCHANT_ID = "500208"
