from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'congreso',
        'USER': 'root',
        'PASSWORD': 'twJuL*2VHoq!c',
        'HOST': 'localhost',
        'PORT': '',
    }
}