from .base import *

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'chef_buddy',
       'USER': 'chefbuddyadmin',
       'PASSWORD': 'chefbuddy123',
       'HOST': 'cooper.cdhlqbkfdy0e.us-west-2.rds.amazonaws.com',
       'PORT': '5432',
       }
}
