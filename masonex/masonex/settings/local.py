import os

from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.163']

INTERNAL_IPS = ['127.0.0.1', '192.168.1.163']

INSTALLED_APPS += ['debug_toolbar', 'django_sass']

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'
