from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import rollbar

load_dotenv()

DEFAULT_CHARSET = 'utf-8'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

MESSAGE_TAGS = {
    'ERROR': 'danger',
}

ROLLBAR_TOKEN = os.getenv('ROLLBAR_TOKEN')

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['*', 'webserver',]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task_manager',
    'django_bootstrap5',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    # 'task_manager.rollbar_middleware.CustomRollbarNotifierMiddleware',
]

ROOT_URLCONF = 'task_manager.urls'

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

WSGI_APPLICATION = 'task_manager.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL, conn_max_age=600, conn_health_checks=True,
    )

AUTH_USER_MODEL = 'task_manager.CustomUser'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = \
    'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LOGIN_URL = '/login/'

ROLLBAR = {
    'access_token': os.getenv('ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
    'patch_debugview': False,
}
