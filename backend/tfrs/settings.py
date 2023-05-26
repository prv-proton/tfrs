"""
Django settings for this project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from pika import ConnectionParameters, PlainCredentials

from . import minio
from . import amqp
from . import email

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    '9e4@&tw46$l31)zrqe3wi+-slqm(ruvz&se0^%9#6(_w3ui!c0'
)

WELL_KNOWN_ENDPOINT = os.getenv('WELL_KNOWN_ENDPOINT',
  'https://dev.loginproxy.gov.bc.ca/auth/realms/standard/.well-known/openid-configuration')

KEYCLOAK_AUDIENCE = os.getenv('KEYCLOAK_AUDIENCE', 'tfrs-on-gold-4308')

UNIT_TESTING_ENABLED = False

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'


# DEVELOPMENT = 'True'
DEVELOPMENT = os.getenv('DEVELOPMENT', 'False') == 'True'

# SECURITY WARNING: never set this on in production
BYPASS_AUTH = os.getenv('BYPASS_HEADER_AUTHENTICATION', False)

TESTING = 'test' in sys.argv
RUNSERVER = 'runserver' in sys.argv


# ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_celery_beat',
    'rest_framework',
    'tfrs',
    'api.app.APIAppConfig',
    'corsheaders',
    'django_nose',
    # 'debug_toolbar',
    # 'nplusone.ext.django',
)

MIDDLEWARE = [
    # 'api.nocache.NoCacheMiddleware',
    "django.middleware.cache.UpdateCacheMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "django.middleware.cache.FetchFromCacheMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', # Uncomment this to enable debug toolbar 
    # 'nplusone.ext.django.NPlusOneMiddleware', # Uncomment this to enable N+1
]
DEBUG_TOOLBAR_PANELS = [
    'ddt_request_history.panels.request_history.RequestHistoryPanel', 
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'RESULTS_STORE_SIZE': 500,
    'HISTORY_LENGTH': 100,
}

# Auth User
AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.keycloak_authentication.UserAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',),
    # 'EXCEPTION_HANDLER': 'core.exceptions.exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',)
}

ROOT_URLCONF = 'tfrs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tfrs/templates'],
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

WSGI_APPLICATION = 'wsgi.application'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

try:
    from . import database
except:
    import database

DATABASES = {
    'default': database.config()
}

AMQP = amqp.config()

AMQP_CONNECTION_PARAMETERS = ConnectionParameters(
    host=AMQP['HOST'],
    port=AMQP['PORT'],
    virtual_host=AMQP['VHOST'],
    credentials=PlainCredentials(AMQP['USER'], AMQP['PASSWORD'])
)

EMAIL = email.config()

MINIO = minio.config()

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DOCUMENTS_API = {
    'ENABLED': bool(
        os.getenv('DOCUMENTS_API_ENABLED', 'False').lower() in ['true', 1]),
}

FUEL_CODES_API = {
    'ENABLED': bool(
        os.getenv('FUEL_CODES_API_ENABLED', 'False').lower() in ['true', 1]),
}

CREDIT_CALCULATION_API = {
    'ENABLED': bool(
        os.getenv('CREDIT_CALCULATION_API_ENABLED', 'False').lower() in ['true', 1]),
}

COMPLIANCE_REPORTING_API = {
    'ENABLED': bool(
        os.getenv('COMPLIANCE_REPORTING_API_ENABLED', 'False').lower() in ['true', 1]),
}

EXCLUSION_REPORTS_API = {
    'ENABLED': bool(
        os.getenv('EXCLUSION_REPORTS_API_ENABLED', 'False').lower() in ['true', 1]),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# We don't use this anywhere
# STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "assets"),
# )

STATIC_URL = '/api/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'DOC_EXPANSION': 'list',
    'APIS_SORTER': 'alpha',
    'SHOW_REQUEST_HEADERS': True
}

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
ALLOWED_HOSTS = ['*']

# CORS Settings

# If True, the whitelist below is ignored and all origins will be accepted
CORS_ORIGIN_ALLOW_ALL = True

# List of origin hostnames that are authorized to make cross-site HTTP requests
CORS_ORIGIN_WHITELIST = ()

# The list of extra HTTP headers to expose to the browser, in addition to the default safelisted headers
CORS_EXPOSE_HEADERS = [
    "Content-Disposition"
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "temp_api_cache",
    },
    'keycloak': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'keycloak',
    },
    'autocomplete': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cached_autocomplete',
        'OPTIONS': {
            'MAX_ENTRIES': 25
        }
    },
    'notification_subscriptions': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cached_notification_subscriptions',
        'TIMEOUT': None,
        'OPTIONS': {
            'MAX_ENTRIES': 100000
        }
    }
}


# Uncomment this stanza to see database calls in the log (quite verbose)
# import logging
# NPLUSONE_LOGGER = logging.getLogger('nplusone')
# NPLUSONE_LOG_LEVEL = logging.WARN
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         },
#         'nplusone': {
#             'handlers': ['console'],
#             'level': 'WARN',
#         }
#     }
# }

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
