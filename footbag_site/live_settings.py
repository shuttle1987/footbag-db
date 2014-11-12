""" This file contains all the settings that are specific to the live deployment site
Note that these settings are used for both the live site and the development staging site.
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

# Database settings, see:
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

with open(os.path.join(BASE_DIR,'mysql_pass.txt')) as f:
    MYSQL_PASS = f.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',#django backend
        'NAME': 'janis$footbag-db-dev',
        'USER': 'janis',
        'PASSWORD': MYSQL_PASS,
        'HOST': 'mysql.server',
    }
}
