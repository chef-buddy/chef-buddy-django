from .base import *
import os

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#
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
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ['RDS_DB_NAME'],
#         'USER': os.environ['RDS_USERNAME'],
#         'PASSWORD': os.environ['RDS_PASSWORD'],
#         'HOST': os.environ['RDS_HOSTNAME'],
#         'PORT': os.environ['RDS_PORT'],
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'tastebud',
#         'PASSWORD': 'tastebud',
#         'HOST': "aasw87elqyv9i7.cq4v2ft4sf6d.us-east-1.rds.amazonaws.com",
#         'PORT': 5432,
#     }
# }
#