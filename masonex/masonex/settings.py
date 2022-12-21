import os
import sys

from pathlib import Path
from dotenv import load_dotenv

from django.urls import reverse_lazy

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'articles.apps.ArticlesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django_editorjs_fields',
    'debug_toolbar',
    'django_sass',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'helpers': 'templatetags.helpers',
            },
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

LOGGING_ROOT = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOGGING_ROOT):
    os.mkdir(LOGGING_ROOT)

GLOBAL_LOG_LEVEL = os.getenv('GLOBAL_LOG_LEVEL', 'WARNING')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} | {asctime} | {name} >> {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'logs.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': GLOBAL_LOG_LEVEL,
            'propagate': False,
        },
        'articles': {
            'handlers': ['console', 'file'],
            'level': GLOBAL_LOG_LEVEL,
            'propagate': False,
        },
    },
    'root': {
       'handlers': ['file'],
       'level': os.getenv('ROOT_LOG_LEVEL', 'ERROR'),
    },
}

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

PHOTOS_PATH = 'photos/%Y/%m/%d/'

EDITORJS_VERSION = '2.26.2'

EDITORJS_DEFAULT_PLUGINS = (
    '@editorjs/paragraph',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/quote',
    '@editorjs/image',
    '@editorjs/code',
    '@editorjs/underline',
    '@editorjs/marker',
    '@editorjs/inline-code',
)

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'paragraph': {
        'class': 'Paragraph',
        'shortcut': 'CMD+SHIFT+A',
    },
    'Header': {
        'class': 'Header',
        'inlineToolbar': False,
        'shortcut': 'CMD+SHIFT+H',
        'config': {
            'placeholder': 'Enter a header',
            'levels': [1, 2, 3, 4],
        },
    },
    'List': {
        'class': 'List',
        'inlineToolbar': True,
        'shortcut': 'CMD+SHIFT+L',
    },
    'Quote': {
        'class': 'Quote',
        'inlineToolbar': True,
        'shortcut': 'CMD+SHIFT+Q',
        'config': {
            'quotePlaceholder': 'Enter the quote',
            'captionPlaceholder': 'Quote by',
        },
    },
    'Code': {
        'class': 'CodeTool',
        'shortcut': 'CMD+SHIFT+C',
    },
    'Image': {
        'class': 'ImageTool',
        'shortcut': 'CMD+SHIFT+U',
        "config": {
            "endpoints": {
                "byFile": reverse_lazy('editorjs_image_upload'),
                "byUrl": reverse_lazy('editorjs_image_by_url')
            }
        },
    },
    'Underline': {
        'class': 'Underline',
        'shortcut': 'CMD+U',
    },
    'InlineCode': {
        'class': 'InlineCode',
        'shortcut': 'CMD+SHIFT+M',
    },
    'Marker': {
        'class': 'Marker',
        'shortcut': 'CMD+SHIFT+E',
    },
}

EDITORJS_CONFIG_OVERRIDE = {
    'inlineToolbar': ('bold', 'italic', 'Underline', 'InlineCode', 'Marker', 'link'),
    'minHeight': 256,
    'i18n': {
        'messages': {
            'toolNames': {
                'InlineCode': 'Monospace',
                'Marker': 'Highlight',
            },
        },
    },
}
