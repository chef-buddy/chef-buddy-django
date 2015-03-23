from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chef_buddy',
        'USER': 'johnmitsch',
        'PASSWORD': 'johnmitsch',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}