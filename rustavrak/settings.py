# -*- coding: utf-8 -*-
# Django settings for rustavrak project.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Sensitive Information.
from config import S_Key, local_post_sql_pw, Post_sql_pw, my_site_id



BASE_DIR = os.path.dirname(__file__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = S_Key

ALLOWED_HOSTS = [
    '.rustavrak.sites.djangoeurope.com',
    '127.0.0.1',
    'conantur.no',
    '.conantur.no',
    'www.conantur.no',
    'rustavrak.no',
    '.rustavrak.no'
]

SITE_ID = my_site_id

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ADMINS = (
    (u'Martin Engen', 'Martin.Engen@outlook.com'),
)

MANAGERS = ADMINS


########### EMAIL #######################
DEFAULT_FROM_EMAIL = 'ikke.svar@rustavrak.no'
SERVER_EMAIL = 'ikke.svar@rustavrak.no'

############ Database Connection ################
if os.getenv('SETTINGS_MODE') == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'rusta_vrak_local',
            'USER': 'local_admin',
            'PASSWORD': local_post_sql_pw
        }
    }
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'nitrax92_rustadb',
            'USER': 'nitrax92',
            'PASSWORD': Post_sql_pw,
            'HOST': '',
            'PORT': '',
        }
    }
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'nb'
TIME_ZONE = 'Europe/Oslo'

# Absolute path to the directory that holds media.
# Example: "/home/username/projectname/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# The absolute path to the directory where collectstatic will collect static files for deployment.
# Example: "/home/username/projectname/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL to use when referring to static files located in STATIC_ROOT.
# Examples: "/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# For static assets that arent't tied to a particular app.
# In addition to using a static/ directory inside your apps, you can define a list of directories
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common_static'),
)

INSTALLED_APPS = (
    'frontpage.apps.FrontpageConfig',
    'cars.apps.CarsConfig',
    'booking.apps.BookingConfig',
    'control_panel.apps.ControlPanelConfig',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'rustavrak.urls'

WSGI_APPLICATION = 'rustavrak.wsgi.application'

# Override the server-derived value of SCRIPT_NAME
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

