# -*- coding: utf-8 -*-
"""
Settings for Django.

Copyright (c) HUDORA. All rights reserved.
"""

# See http://docs.djangoproject.com/en/dev/ref/settings/ for inspiration

import os
import django

from cs.global_django_settings import *
from settings_local import *

OUR_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
if os.environ.get('SILVER_VERSION', '').startswith('silverlining/'):
    # we are running on a silverlining managed production server.
    # see http://cloudsilverlining.org/services.html#silver-version-environmental-variable
    DEBUG = False

TEMPLATE_DEBUG = DEBUG
if DEBUG:
    TEMPLATE_STRING_IF_INVALID = "__%s__"
else:
    SEND_BROKEN_LINK_EMAILS = True

MEDIA_URL = 'http://s.hdimg.net/taskmaster/'
# for development you can use something like this:
# MEDIA_ROOT = './public/'
# MEDIA_URL = '/public/'


ROOT_URLCONF = 'urls'
SITE_ID = 2 # intern.hudora.biz


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments', 
    'django.contrib.markup',
    'debug_toolbar',
    'taskmaster',
)


# TEMPLATE_DIRS = (
#     os.path.join(SITE_ROOT, 'generic_templates')
#     '/usr/local/www/www_intern/generic_templates/'
# )


TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'googleappsauth.middleware.GoogleAuthMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(OUR_ROOT, 'generic_templates'),
)


LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/main'
LOGOUT_URL = '/logout'
AUTHENTICATION_BACKENDS = ('googleappsauth.backends.GoogleAuthBackend',)
GOOGLE_OPENID_REALM = 'http://asksheila.org/'
if not os.environ.get('SILVER_VERSION', '').startswith('silverlining/'):
    GOOGLE_OPENID_REALM = 'http://127.0.0.1:8080/'

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.environ['CONFIG_FILES'], 'taskmaster.db')

SERVER_EMAIL = 'm.dornseif+server@hudora.de'
EMAIL_HOST = 'mailout.easydns.com'
EMAIL_USE_TLS = True

ADMINS = (
    ('md', 'm.dornseif+django@hudora.de'),
)
MANAGERS = ADMINS
PREPEND_WWW = False

#### begin defaults ####

# default settings which should be the same for most Django applications at Hudora
import os

ADMIN_MEDIA_PREFIX = 'http://s.hdimg.net/djangoadmin/1.0.2/'
INTERNAL_IPS = ('127.0.0.1')

TIME_FORMAT = 'H:i'
TIME_ZONE = 'Europe/Amsterdam'
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'
USE_I18N = True
LANGUAGE_CODE = 'de-de'
LANGUAGES = (
  ('zh', 'Chinese'),
  ('de', 'German'),
  ('en', 'English'),
)


SECRET_KEY = 'sua1+khy2x-dojd_+r2j^7$asdfasQ@#$)!v94tpxe-g&_n6xxxv0!f+y'

