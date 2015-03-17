import random
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from chef_buddy.models import Recipe, UserFlavorCompound, IngredientFlavorCompound


_app_id = '844ee8f7'
_app_key = '9b846490c7c34c4f33e70564831f232b'


@api_view(['GET'])
def show_top_recipe(request):
    """Manages actual top recipe request process"""
    raw_yum_recipes = get_yummly_recipes() #grab recipes
    user_data = find_user_fc_ids(1) #grab user food compounds
    rec_object, rec_food_compounds = rec_engine(raw_yum_recipes, user_data) # pick top recipe for user
    #store_recipe_fc(rec_object['id'], rec_food_compounds) #stores recipe_id to fc in database
    return Response(rec_object) #returns recipe object to requester


def get_yummly_recipes():
    request_amount = 40 #  change for amount of recipes returned from yummly
    recipes = get_recipes(request_amount)
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
    """recipe_list = raw list of recipes directly from yummly
    takes in a list of recipes and returns a tupled list of recipe_id, ingredient"""
    return [(recipe['id'], ingredient) for recipe in recipe_list for ingredient in recipe['ingredients']]


def recipes_to_fc_id(recipe_list):
    """ recipe_list = Raw Recipe input from yummly
    Takes in a list of recipes and returns a tupled list of recipe_id to flavor compound id"""
    recipe_ingr_list = recipe_ingr_parse(recipe_list)
    recipe_fc_list = []
    for recipe_id, ingredient in recipe_ingr_list:
        flavors = IngredientFlavorCompound.objects.filter(ingredient_id=ingredient)
        for fc_id in flavors:
            recipe_fc_list.append((recipe_id,fc_id.flavor_id))
    return recipe_fc_list


def find_user_fc_ids(user_id=1):
    """user_id = id of user in question
    Looks up all the user's flavor compounds and associated scores. Returns them in a tupled list.
    Also returns list of flavor compounds for that recipe"""
# This is another one dummy
    flavor_compounds = UserFlavorCompound.objects.filter(user_id=user_id)
    return {flavor.flavor_id: flavor.score for flavor in flavor_compounds}


def rec_engine(raw_recipes, user_fc_data):
    """raw_recipes = list of raw recipes from yummly
    user_fc_data = user to food compound dict
    This function is the engine for picking a recipe given a user's food compounds. Returns 1 recipe object."""
    recipe_id_fc_list = recipes_to_fc_id(raw_recipes)

    match_dict = user_to_recipe_counter(recipe_id_fc_list, user_fc_data)
    rec_id = max(match_dict, key=match_dict.get)
    rec_id_fc_list = [fc_id for recipe_id, fc_id in recipe_id_fc_list if recipe_id == rec_id]
    return recipe_id_to_object(rec_id, raw_recipes), rec_id_fc_list


def recipe_id_to_object(recipe_id, recipe_list):
    """Looks recipe_id in recipe_list and returns recipe object"""
    for recipe in recipe_list:
        if recipe['id'] == recipe_id:
            return recipe


def user_to_recipe_counter(recipe_id_fc_list, user_fc_data):
    """Takes in user's flavor compounds and recipe flavor compounds to produce a dict of how
    many times the flavor compounds of the user appear in each recipe for the user. Each time
    a flavor compound appears, the score associated with the user's fc will be added to the recipe"""

    match_dict = {recipe_id:0 for recipe_id, fc_id in recipe_id_fc_list}
    recipe_fc_count = 0
    for recipe_id, fc_id in recipe_id_fc_list:
        if fc_id in user_fc_data.keys():
            match_dict[recipe_id] += user_fc_data[fc_id]
            recipe_fc_count += 1

    normalize_fc_count(match_dict, recipe_fc_count)
    return match_dict

# def store_recipe_fc(recipe_id, flavor_compounds):
#     """recipe_id = id of the recipe needing to be housed
#     flavor_compounds = list of flavor compounds associated with recipe
#     This function is designed to take the above variables and store them in separate rows in the db"""
#     for fc_id in flavor_compounds:
#         if fc_id in database:
# #This still needs help!
#     return True

def normalize_fc_count(match_count_dict, recipe_to_fc_count):
    """Normalizes for a recipe simply having a lot of food compounds"""
    normalized = match_count_dict.copy()
    for recipe_id, score in match_count_dict.items():
        if normalized[recipe_id] > 0:
            normalized[recipe_id] = normalized[recipe_id] / recipe_to_fc_count
    return normalized

def log_recommendation(to_be_written):
    print(to_be_written)
    return True
