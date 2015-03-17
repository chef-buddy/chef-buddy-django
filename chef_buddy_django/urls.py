import random

from django.conf.urls import patterns, include, url
from django.contrib import admin
from chef_buddy.models import Recipe
from rest_framework import routers, serializers, viewsets, generics


urlpatterns = patterns('chef_buddy.views',
    url(r'^api/v1/suggested_recipe/$', 'show_top_recipe'),
    url(r'^admin/', include(admin.site.urls))
)
