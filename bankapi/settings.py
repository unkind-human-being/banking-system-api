"""
Django settings for bankapi project (production-ready).
"""

import os
from pathlib import Path
import dj_database_url  # ✅ to parse DATABASE_URL from Render
from django.core.management.utils import get_random_secret_key

# --------------------------
# Basic Setup
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allow Render or any domain you use
ALLOWED_HOSTS = ['*']

# --------------------------
# Installed Apps
# --------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',

    # Local apps
    'accounts',
]

# --------------------------
# Middleware
# --------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ✅ WhiteNoise for static file serving
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bankapi.urls'

# --------------------------
# Templates
# --------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # you can add template directories here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bankapi.wsgi.application'

# --------------------------
# Database
# --------------------------
# Use Render’s DATABASE_URL, fallback to local Postgres
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'postgres://postgres:abdul@localhost:5432/bankdb'),
        conn_max_age=600,
        ssl_require=False  # Render automatically enforces SSL
    )
}

# --------------------------
# Password validation
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------
# Localization
# --------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------------
# Static Files
# --------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise static file compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------
# Default Auto Field
# --------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
