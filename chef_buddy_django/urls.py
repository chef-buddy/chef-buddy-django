import random

from django.conf.urls import patterns, include, url
from django.contrib import admin
from chef_buddy.models import Recipe
from rest_framework import routers, serializers, viewsets, generics


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('recipe_title', 'recipe_link', 'recipe_image')

urlpatterns = patterns('chef_buddy.views',
    url(r'^api/v1/random_recipe/$', 'get_random_recipe'),
    url(r'^admin/', include(admin.site.urls))
)
