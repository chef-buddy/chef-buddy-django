from .base import *
import os

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'tastebud',
#         'USER': 'tastebud',
#         'PASSWORD': 'tastebud',
#         'HOST': 'mysql.server',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tastebud',
        'USER': 'tastebud',
        'PASSWORD': os.environ['PASSWORD'],
        'HOST': os.environ['HOST'],
        'PORT': 5432,
    }
}
