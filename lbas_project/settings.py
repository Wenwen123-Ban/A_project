import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'lbas-django-secret-key-change-in-production-2024'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'core',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lbas_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'lbas_project.wsgi.application'

# ── Database: try MySQL (XAMPP), fall back to SQLite ──────────────
def _try_mysql():
    """Return True if MySQL/XAMPP lbas_db is reachable."""
    try:
        import MySQLdb
        c = MySQLdb.connect(host='127.0.0.1', port=3306, user='root',
                            passwd='', db='lbas_db', connect_timeout=2)
        c.close()
        return True
    except Exception:
        pass
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb as _m
        c = _m.connect(host='127.0.0.1', port=3306, user='root',
                       passwd='', db='lbas_db', connect_timeout=2)
        c.close()
        return True
    except Exception:
        return False


if _try_mysql():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'lbas_db',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'connect_timeout': 5,
                # Satisfies MariaDB W002 — enforces data integrity (no silent truncation)
                'sql_mode': 'STRICT_TRANS_TABLES',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = False
USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/profile/'
MEDIA_ROOT = BASE_DIR / 'Profile'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[LBAS] %(levelname)s %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'LBAS': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        'django.request': {'handlers': ['console'], 'level': 'WARNING'},
        'django.db.backends': {'handlers': ['console'], 'level': 'WARNING'},
    },
}
