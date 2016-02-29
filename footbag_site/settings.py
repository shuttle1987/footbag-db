"""
Django settings for footbag_site project.

This settings file contains all the settings that are shared between all
environments (in this case dev and live) then imports the deployment specific settings
from local_settings.py.

local_settings.py just imports the relevant settings for the deployment and as such is
different in each deployment. local_settings.py is not tracked by git for this reason.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#Use the following live settings to build on Travis CI
if os.getenv('BUILD_ON_TRAVIS', None):
    SECRET_KEY = "SecretKeyForUseOnTravis"
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',#django backend
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
        }
    }
else:
    #import the settings specific to the environment (dev or live)
    from .local_settings import *
    with open(os.path.join(BASE_DIR,'secret_key.txt')) as f:
        SECRET_KEY = f.read().strip()

# Rendering for the trick tips via markdownfield
import markdown
import bleach

from docutils.core import publish_parts

#settings for Bleach
bleach_tags_allowed = [
    'br',
    'p',
    'em',
    'strong',
]

def render_rest(markup):
    """ Render ReStructuredText to HTML then clean the output using Bleach.
    This is to prevent a number of issues to do with XSS."""
    parts = publish_parts(source=markup, writer_name="html4css1")
    return bleach.clean(parts["fragment"], bleach_tags_allowed)

#settings for markdown
markdown_extensions = [
    "nl2br",#makes newlines appear as </br>, this is probably what the users expect
]

def render_markdown_clean(markup):
    """ Render markdown to HTML then clean the output using Bleach.
    This is to prevent a number of issues to do with XSS."""
    return bleach.clean(markdown.markdown(markup, markdown_extensions), bleach_tags_allowed)

MARKUP_FIELD_TYPES = (
    ('markdown', render_markdown_clean),
    ('ReST', render_rest),
)


ACCOUNT_OPEN_SIGNUP = False#django-user-accounts, this sets the site to private beta mode and requires signups to have tokens.



ALLOWED_HOSTS = ['.footbag.info',
                 '.footbag.info.',
                ]


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'account',#django-user-accounts
    'markupfield',#django-markupfield
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
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.LocaleMiddleware',#django-user-accounts
    'account.middleware.TimezoneMiddleware',#django-user-accounts
)

ROOT_URLCONF = 'footbag_site.urls'

WSGI_APPLICATION = 'footbag_site.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'footbag_site', 'static'),)

# Location of template files
TEMPLATE_DIRS = (    
    os.path.join(BASE_DIR, 'footbag_site', 'templates'),
    os.path.join(BASE_DIR, 'apps', 'home', 'templates'),
    os.path.join(BASE_DIR, 'apps', 'footbagmoves', 'templates'),
    os.path.join(BASE_DIR, 'user_accounts', 'templates'),
)

TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + [
    "account.context_processors.account",#django-user-accounts
]

