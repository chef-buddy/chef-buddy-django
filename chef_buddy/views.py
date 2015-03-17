import random
import requests
import pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from chef_buddy.models import Recipe
from chef_buddy_django.urls import RecipeSerializer


_app_id = '844ee8f7'
_app_key = '9b846490c7c34c4f33e70564831f232b'
pp = pprint.PrettyPrinter(indent=4)
# Create your views here.



@api_view(['GET'])
def get_random_recipe(request):
    if request.method == 'GET':
        random_idx = random.randint(0, Recipe.objects.count() - 1)
        recipe = Recipe.objects.all()[random_idx]
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

@api_view(['GET'])
def get_yummly_recipes(request):
    request_amount = 40 #  change for amount of recipes returned from yummly
    recipes = get_recipes(40)
    recipe_list = recipes['matches'][random.randint(1, request_amount)]
    return Response(recipe_list)

def get_recipes(amount):
    random_start = random.randint(1, (321961 - amount))
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes',
                               params={'_app_id':_app_id,
                                       '_app_key':_app_key,
                                       'maxResult':amount,
                                       'requirePictures':'true',
                                       'start':random_start })
    return all_recipes.json()
