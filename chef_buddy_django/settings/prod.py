from .base import *
import os

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'chef_buddy',
       'USER': 'chefbuddyadmin',
       'PASSWORD': os.environ['PASSWORD'],
       'HOST': os.environ['HOST'],
       'PORT': '5432',
       }
}
