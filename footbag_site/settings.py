"""
Django settings for footbag_site project.

This settings file contains all the settings that are shared between all
environments (in this case dev and live) then imports the deployment specific settings
from local_settings.py.

local_settings.py just imports the relevant settings for the deployment and as such is
different in each deployment. local_settings.py is not tracked by git for this reason.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from local_settings import * #import the settings specific to the environment (dev or live)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '4iz9)#m9^4g71o@z3z1oqq^#rk7&vz&r%8bo3l9v41#fhjhe0_'
with open('/home/janis/footbag_secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

ALLOWED_HOSTS = ['.footbag.info',
                 '.footbag.info.',
                ]


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'south',
)

LOCAL_APPS = (
    'apps.footbagmoves',
    'apps.home',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'footbag_site.urls'

WSGI_APPLICATION = 'footbag_site.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Location of template files
TEMPLATE_DIRS = (    
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
)

