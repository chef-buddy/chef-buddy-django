import random
import requests
import json
import time
from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from chef_buddy.models import Recipe, UserFlavorCompound, IngredientFlavorCompound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import F
from multiprocessing import Pool


_app_id = '844ee8f7'
_app_key = '9b846490c7c34c4f33e70564831f232b'

def speed_test(func):
    """wrapper function for testing speed"""
    def wrapper(*args, **kwargs):
        t1 = time.time()
        for x in range(1):
            results = func(*args, **kwargs)
        t2 = time.time()
        total_time = t2-t1
        print('\n')
        print('{} took {} seconds'.format(func.__name__, total_time))
        return results
    return wrapper


@api_view(['GET', 'POST'])
@method_decorator(csrf_exempt)
@speed_test
def show_top_recipe(request):
    """Manages actual top recipe request process"""
    post = request.POST.copy()
    user, liked, recipe = post.get('user', 1), post.get('liked', 0), post.get('recipe', '')
    store_user_fc(user, recipe, liked)
    user_fc_dict, recipe_id_fc_dict, raw_recipes = pre_engine(user)
    normalized_list = rec_engine(recipe_id_fc_dict, user_fc_dict, 1)
    final_rec_result = post_engine(normalized_list, recipe_id_fc_dict, raw_recipes, user_fc_dict)
    # pool = Pool()
    # result1 = pool.apply_async(get_yummly_recipes, [])
    # result2 = pool.apply_async(store_user_fc, args=(user, recipe, liked))
    # recipes = result1.get(timeout=10)
    return Response(final_rec_result)

@api_view(['GET', 'POST'])
@method_decorator(csrf_exempt)
@speed_test
def recipe_list(request):
    """Returns a list of suggested recipes"""
    post = request.POST.copy()
    user = post.get('user', 1)
    user_fc_dict, recipe_id_fc_dict, raw_recipes = pre_engine(user)
    normalized_list = rec_engine(recipe_id_fc_dict, user_fc_dict, 12)
    final_rec_result = post_engine(normalized_list, recipe_id_fc_dict, raw_recipes, user_fc_dict)
    return Response(final_rec_result)

@speed_test
def pre_engine(user):
    user_fc_dict = find_user_fc_ids(user)
    raw_recipes = get_yummly_recipes()
    recipe_id_fc_dict = recipes_to_fc_id(raw_recipes)
    return user_fc_dict, recipe_id_fc_dict, raw_recipes

@speed_test
def rec_engine(recipe_id_fc_dict, user_fc_dict, amount):
    """raw_recipes = list of raw recipes from yummly
    user_fc_dict = user to food compound dict
    amount = how many recipes to return
    This function is the engine for picking a recipe given a user's food compounds.
    Returns recipe object(s)."""
    match_list = user_to_recipe_counter(recipe_id_fc_dict, user_fc_dict)
    normalized_list = normalize_fc_count(match_list, recipe_id_fc_dict)
    normalized_list = normalized_list[:amount]
    return normalized_list

@speed_test
def post_engine(normalized_list, recipe_id_fc_dict, raw_recipes, user_fc_dict):
    [store_recipe_fc(recipe_id, recipe_id_fc_dict[recipe_id]) for recipe_id, score in normalized_list]
    rec_object_list = []
    for recipe_id, score in normalized_list:
        rec_object = recipe_id_to_object(recipe_id, raw_recipes)
        rec_object['recommendation_score'] = score_recommendation(recipe_id_fc_dict[recipe_id], user_fc_dict)
        rec_object = large_image(rec_object)
        rec_object_list.append(rec_object)
    return rec_object_list

@api_view(['GET'])
def random_recipe(request):
    recipe_list = get_yummly_recipes()
    recipe = recipe_list[random.randint(1, 10)]
    recipe = large_image(recipe)
    return Response(recipe)


def get_yummly_recipes():
    recipes = get_recipes(10)
    return recipes['matches']


def get_recipes(amount):
    random_start = random.randint(1, (321961 - amount))
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes',
                               params={'_app_id':_app_id, '_app_key':_app_key,
                                       'maxResult':amount, 'requirePictures':'true',
                                       'start':random_start })
    return all_recipes.json()


def large_image(json):
    """
    Takes the image from the Yummly api and returns a larger image by changing the URL.
    :return: json object
    """
    image = json["imageUrlsBySize"]['90']
    json['largeImage'] = image.replace('=s90-c', '=s600')
    return json


def recipe_ingr_parse(recipe_list):
    """recipe_list = raw list of recipes directly from yummly
    takes in a list of recipes and returns a dict of recipe_id, [ingredients]"""
    recipe_ingredient_dict = {}
    for recipe in recipe_list:
        recipe_ingredient_dict[recipe['id']]= [ingredient for ingredient in recipe['ingredients']]
    return recipe_ingredient_dict


def recipes_to_fc_id(recipe_list):
    """ recipe_list = Raw Recipe input from yummly
    Takes in a list of recipes and returns a tupled list of recipe_id to flavor compound id"""
    recipe_ingr_dict = recipe_ingr_parse(recipe_list)
    recipe_fc_dict = {}
    for recipe, ingredients in recipe_ingr_dict.items():
        flavor_compounds = IngredientFlavorCompound.objects.filter(ingredient_id__in=ingredients).values_list('flavor_id', flat=True)
        recipe_fc_dict[recipe] = flavor_compounds
    return recipe_fc_dict


def check_for_recipe(recipe_id):
    """
    checks to see if recipe is stored in local database
    :param recipe_id:
    :return:
    """


def store_user_fc(user_id, recipe_id, taste):
    """Takes a user_id, recipe_id, and taste (should be a 1 or -1). It will lookup the recipe_id in the
    database to find associated food compounds. It will then lookup to see if the user has already liked
    disliked those flavor compounds. If they've liked them before, then it will update the score. If not,
    It will create a new row for that food compound."""
    user_id, taste = int(user_id), int(taste)

    if taste in [-1, 1]:
        flavor_compounds = Recipe.objects.filter(recipe_id=recipe_id).values_list('flavor_id', flat=True)
        exists = UserFlavorCompound.objects.filter(user_id=user_id, flavor_id__in=flavor_compounds)\
                                           .values_list('flavor_id', flat=True)
        UserFlavorCompound.objects.filter(user_id=user_id, flavor_id__in=exists).update(score=F('score') + taste)
        update_fc = [num for num in set(flavor_compounds) if num not in set(exists)]
        UserFlavorCompound.objects.bulk_create([UserFlavorCompound(user_id=user_id,flavor_id=flavor,
                                                                   score=taste) for flavor in update_fc])
    return True


def find_user_fc_ids(user_id=1):
    """user_id = id of user in question
    Looks up all the user's flavor compounds and associated scores. Returns them in a dict.
    Also returns list of flavor compounds for that recipe. If the user doesn't have any flavor
    compounds, then we'll return a random recipe (one that is derived from user 1's flavor compounds)"""
    try:
        flavor_compounds = UserFlavorCompound.objects.filter(user_id=user_id)
        return {flavor.flavor_id: flavor.score for flavor in flavor_compounds}
    except UserFlavorCompound.DoesNotExist:
        flavor_compounds = UserFlavorCompound.objects.filter(user_id=1)
        return {flavor.flavor_id: flavor.score for flavor in flavor_compounds}


def recipe_id_to_object(recipe_id, recipe_list):
    """Looks recipe_id in recipe_list and returns recipe object"""
    for recipe in recipe_list:
        if recipe['id'] == recipe_id:
            return recipe


def user_to_recipe_counter(recipe_id_fc_dict, user_fc_dict):
    """Takes in user's flavor compounds and recipe flavor compounds to produce a dict of how
    many times the flavor compounds of the user appear in each recipe for the user. Each time
    a flavor compound appears, the score associated with the user's fc will be added to the recipe"""
    user_fc_dict_positive = [key for key in user_fc_dict.keys() if user_fc_dict[key] > 0]
    match_list = []
    for recipe_id, fc_id_list in recipe_id_fc_dict.items():
        matched = set.intersection(set(user_fc_dict_positive),set(fc_id_list))
        match_list.append((recipe_id, len(matched)))
    return match_list


def store_recipe_fc(recipe_id, flavor_compounds):
    """recipe_id = id of the recipe needing to be housed
    flavor_compounds = list of flavor compounds associated with recipe
    This function is designed to take the above variables and store them in separate rows in the db"""
    if not Recipe.objects.filter(recipe_id=recipe_id):
        recipe_list = [Recipe(recipe_id=recipe_id, flavor_id=fc_id) for fc_id in flavor_compounds]
        Recipe.objects.bulk_create(recipe_list)
    return True


def normalize_fc_count(match_list, recipe_id_fc_dict):
    """Normalizes scores for recipes simply having a lot of food compounds"""
    normalized_list = []
    for recipe_id, score in match_list:
        if score > 0:
            fc_count = len(recipe_id_fc_dict[recipe_id])
            normalized_list.append((recipe_id,(score/ fc_count)))
    return sorted(normalized_list, key=lambda x: x[1], reverse=True)


def log_recommendation(dict_of_logs):
    with open('chef_buddy/raw_data/rec_log.txt', 'a') as the_file:
        the_file.write(str(datetime.now()))
        the_file.write('\n')
        for header, log in dict_of_logs.items():
            the_file.write(header)
            the_file.write('\n\n')
            the_file.write(str(log))
            the_file.write('\n\n')
        the_file.write('\n\n\n\n\n')
    return True


def score_recommendation(rec_fc_list, user_fc_data):
    """This function takes in the recommended recipe and it's food compounds, and the total food
    compounds the user has. It will remove any negative user to food compound relationships, then produce
    a score of how many food compounds of the chosen recipe were already chosen by the user."""
    hit_list = [user_fc for user_fc in user_fc_data.keys()
                if user_fc in rec_fc_list and user_fc_data[user_fc] > 0]
    return len(hit_list) / len(set(rec_fc_list)) * 100
