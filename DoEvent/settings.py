"""
Django settings for DoEvent project.
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-v!uqwi9bowhf5nao^5mr4hnb4#b(j_8isshw^&ses23xgat3s2')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'Kullanıcılar',
    'Core',
    'Akademik.AkademikTakvim',
    'Akademik.DevamsizlikTakvimi',
    'Akademik.RandevuSistemi',
    'Akademik',
    'Sosyal',
    'Sosyal.Etkinlik',
    'Sosyal.EtkinlikOner',
    'Sosyal.Kulup',
    'Sosyal.KulupOner',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DoEvent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'DoEvent.wsgi.application'

# Database - SQLite for Django (users, auth, sessions)
# MongoDB for application data (accessed via pymongo in views)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB connection for app data
from pymongo import MongoClient

MONGODB_URI = config('MONGODB_URI', default='mongodb://localhost:27017/')
MONGODB_DB_NAME = config('MONGODB_DB_NAME', default='dogustansosyalDB')

try:
    mongodb_client = MongoClient(MONGODB_URI)
    mongodb_db = mongodb_client[MONGODB_DB_NAME]
    print(f"MongoDB baglantisi basarili: {MONGODB_DB_NAME}")
except Exception as e:
    print(f"MongoDB baglanti hatasi: {e}")
    mongodb_db = None

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'Kullanıcılar' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
