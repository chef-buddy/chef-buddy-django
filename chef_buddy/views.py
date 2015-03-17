import random
import requests
import pprint
import timeit
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from chef_buddy.models import Recipe
from chef_buddy_django.urls import RecipeSerializer
from chef_buddy.ingredient_fc_id import ingredient_to_fc_dict


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

#@api_view(['GET'])
def get_yummly_recipes():
    request_amount = 40 #  change for amount of recipes returned from yummly
    recipes = get_recipes(40)
    recipe_list = recipes['matches']
    return recipe_list

def get_recipes(amount):
    random_start = random.randint(1, (321961 - amount))
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes',
                               params={'_app_id':_app_id,
                                       '_app_key':_app_key,
                                       'maxResult':amount,
                                       'requirePictures':'true',
                                       'start':random_start })
    return all_recipes.json()


def recipe_ingr_parse(recipe_list):
    return [(recipe['id'], ingredient) for recipe in recipe_list for ingredient in recipe['ingredients']]


def fc_return(recipe_id, ingredient):
    # will need to look in db table long term instead of dict.
    return [(recipe_id, fc_id) for fc_id in ingredient_to_fc_dict[ingredient]]


def recipe_fc_single_return(recipe_ingr_list):
    recipe_fc_final = []
    for recipe_id, ingredient in recipe_ingr_list:
        if ingredient in ingredient_to_fc_dict.keys():
            recipe_fc_final.extend(fc_return(recipe_id, ingredient))
    return recipe_fc_final


def recipe_list_fc_id(recipe_list):
    recipe_ing = recipe_ingr_parse(recipe_list)
    recipe_fc_id = {recipe['id']: [] for recipe in recipe_list}
    for recipe_id, fc_id in recipe_fc_single_return(recipe_ing):
        if recipe_id in recipe_fc_id:
            recipe_fc_id[recipe_id].append(fc_id)
    return recipe_fc_id


def get_top_recipe_for_user(raw_recipes, user_fc_data):
    recipe_id_fc_list = recipe_list_fc_id(raw_recipes)
    recipe_to_fc_count = {recipe_id:0 for recipe_id in recipe_id_fc_list.keys()}

    for recipe_id, flavor_comp_id in recipe_id_fc_list.items():

        for user_flav, user_score in user_fc_data:
            if user_flav in flavor_comp_id:
                recipe_to_fc_count[recipe_id] += user_score

    return max(recipe_to_fc_count, key=recipe_to_fc_count.get)


@api_view(['GET'])
def show_top_recipe(request):
    raw_yum_recipes = get_yummly_recipes()
    fake_user_data = [(748, 1), (879, 4), (50, 2), (3,8), (59,1), (200,2)]
    rec_id = get_top_recipe_for_user(raw_yum_recipes, fake_user_data)
    for recipe in raw_yum_recipes:
        if recipe['id'] == rec_id:
            return Response(recipe)
  
