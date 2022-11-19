import os
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9(=z-=^wn=k%_7wvls6spp=fl^%d181@8pp=*-&hb)9-#=f$s3'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django_sass',
    'debug_toolbar',
    'django_editorjs_fields',
    'hitcount',
    'feed.apps.FeedConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'masonex.urls'

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

WSGI_APPLICATION = 'masonex.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

AUTH_USER_MODEL = 'feed.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

PHOTOS_PATH = 'photos/%Y/%m/%d/'

EDITORJS_CONFIG = {
    'plugins': [
        '@editorjs/paragraph',
        '@editorjs/header',
        '@editorjs/list',
        '@editorjs/quote',
        '@editorjs/image',
        '@editorjs/inline-code',
        '@editorjs/underline',
        'editorjs-strikethrough',
    ],
    'tools': {
        'Header': {
            'class': 'Header',
            'config': {
                'placeholder': 'Enter heading',
                'levels': [2, 3],
                'defaultLevel': 2,
            }
        },
        'Quote': {
            'class': 'Quote',
            'inlineToolbar': True,
            'shortcut': 'CMD+SHIFT+O',
            'config': {
                'quotePlaceholder': 'Enter the quote',
                'captionPlaceholder': 'Quote by...',
            },
        },
        'Underline': {
            'class': 'Underline',
            'shortcut': 'CMD+U',
        },
        'strikethrough': {
            'class': 'Strikethrough',
            'shortcut': 'CMD+SHIFT+X',
        },
        'InlineCode': {
            'class': 'InlineCode',
            'shortcut': 'CMD+SHIFT+M',
        },
    },
    'inlineToolbar': ('bold', 'italic', 'Underline', 'strikethrough', 'InlineCode', 'link'),
    'minHeight': 156,
    'i18n': {
        'messages': {
            'toolNames': {
                'InlineCode': 'Monospace',
                'Strikethrough': 'Cross',
            },
        },
    },
}
