from .base import *

DEBUG = True

ALLOWED_HOSTS = [ '127.0.0.1', '0.0.0.0', 'localhost', 'localhost:3000', 'http://localhost:3000', 'http://127.0.0.1:3000', '127.0.0.1:3000' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'