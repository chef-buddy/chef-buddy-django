import random
import requests
import json
import time
import numpy as np
from datetime import datetime
from sklearn.svm import LinearSVC
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from chef_buddy.models import Recipe, UserFlavorCompound, IngredientFlavorCompound, Recipe
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
    user, liked, recipe = post.get('user', 0), post.get('liked', 0), post.get('recipe', '')

    store_user_recipe(user, recipe, liked)
    recipes = get_yummly_recipes()
    if not UserFlavorCompound.objects.filter(user_id=user):
        return Response(recipes[0])
    likes_dislikes, fc_list_lists, recipe_fc_dict = engine_prep(user, recipes)
    rec_list = classify_recipes(likes_dislikes, fc_list_lists, recipe_fc_dict)
    rec_answer = post_engine_prep(rec_list, recipes, recipe_fc_dict, amount=1)
    return Response(rec_answer[0])


def engine_prep(user, raw_recipes):
    """
    Breaks down incoming yummly recipes into dict: {recipe_id:[flavor compounds]}
    Creates list of likes: [1,0,0,1,0,1]
    Creates list of flavor compound lists: [[flavorcompounds], [flavorcompounds]]
    """
    recipes = UserFlavorCompound.objects.filter(user_id=user)
    classifiers = classifier_creation(user)
    likes_dislikes = UserFlavorCompound.objects.filter(recipe__recipe_id__in=recipes).values_list('liked')
    recipe_fc_dict = recipes_to_fc_id(raw_recipes)
    return likes_dislikes, classifiers, recipe_fc_dict


def classify_recipes(likes_dislikes, fc_list_lists, recipe_fc_dict):
    clf = LinearSVC()
    clf.fit(fc_list_lists, likes_dislikes)
    recipe_scores = []
    for recipe, compounds in recipe_fc_dict.items():
        prediction = clf.predict(compounds)
        score = clf.decision_function(compounds)
        recipe_scores.append((recipe, score))
    return recipe_scores


def classifier_creation(user):
    recipes = UserFlavorCompound.objects.filter(user_id=user).values_list('recipe_id', flat=True)
    classifiers = np.zeros((1107,), dtype=np.int)
    for recipe in recipes:
        bare_list = np.zeros((1107,), dtype=np.int)
        for flavor_id in Recipe.objects.filter(recipe_id=recipe).values_list('flavor_id'):
            bare_list[flavor_id] = 1
        classifiers.concatenate((classifiers, bare_list))
    return classifiers


def post_engine_prep(rec_tuple_list, recipe_list, recipe_fc_dict, amount=1):

    rec_tuple_list = rec_tuple_list[0:amount]
    [store_recipe_fc(rec_id, recipe_fc_dict[rec_id]) for rec_id, score in rec_obj_list]
    rec_obj_list = [(recipe_id_to_object(rec_id, recipe_list),rec_score) for rec_id, rec_score in rec_tuple_list]

    # log_recommendation({'raw recipes':[(recipe['id'],recipe['ingredients']) for recipe in recipes],
    #                     'user to fc data':user_data,
    #                     'final predicted recipe':[rec_object['id'],rec_object['ingredients']],
    #                     'food compounds of chosen recipe':rec_food_compounds})
    print(sorted(rec_obj_list, key=lambda x: x[1], reverse=True))
    return sorted(rec_obj_list, key=lambda x: x[1], reverse=True)


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
    Takes in a dict of recipes and returns a dict of recipe_id to [flavor compound ids]"""
    recipe_ingr_dict = recipe_ingr_parse(recipe_list)
    recipe_fc_dict = {}
    for recipe, ingredients in recipe_ingr_dict.items():
        recipe_fc_dict[recipe] = np.array([IngredientFlavorCompound.objects.filter(ingredient_id__in=ingredients)\
                                                                 .values_list('flavor_id', flat=True)])
    return recipe_fc_dict


def liked_bool(liked):
    if liked == "1":
        return True
    elif liked == "-1":
        return False


def store_user_recipe(user_id, recipe_id, liked):
    """Takes a user_id, recipe_id, and liked (should be a 1 or -1). It will update the user to recipe
    table given the inputs."""
    print(liked)
    user_id, liked = int(user_id), liked_bool(liked)
    print("bool {}".format(liked))
    if liked in [-1, 1] and recipe_id:
        obj = Recipe.objects.filter(recipe_id=recipe_id)
        if obj:
            user_recipe = UserFlavorCompound(user_id=user_id, recipe=obj, liked=liked)
            user_recipe.save()
            return True
    else:
        return False


def find_user_fc_ids(user_id=1):
    """user_id = id of user in question
    Looks up all the user's flavor compounds and associated scores. Returns them in a tupled list.
    Also returns list of flavor compounds for that recipe. If the user doesn't have any flavor
    compounds, then we'll return a random recipe (one that is derived from user 1's flavor compounds)"""
    try:
        flavor_compounds = UserFlavorCompound.objects.filter(user_id=user_id)
        return {flavor.flavor_id: flavor.score for flavor in flavor_compounds}
    except UserFlavorCompound.DoesNotExist:
        flavor_compounds = UserFlavorCompound.objects.filter(user_id=1)
        return {flavor.flavor_id: flavor.score for flavor in flavor_compounds}


def recipe_id_to_object(recipe_id, recipe_list):
    """Looks recipe_id in recipe_list and returns recipe object with fixed image size"""
    for recipe in recipe_list:
        if recipe['id'] == recipe_id:
            rec_object = large_image(recipe)
            return rec_object


def store_recipe_fc(recipe_id, flavor_compounds):
    """recipe_id = id of the recipe needing to be housed
    flavor_compounds = list of flavor compounds associated with recipe
    This function is designed to take the above variables and store them in separate rows in the db"""
    if not Recipe.objects.filter(recipe_id=recipe_id):
        recipe_list = [Recipe(recipe_id=recipe_id, flavor_id=fc_id) for fc_id in flavor_compounds]
        Recipe.objects.bulk_create(recipe_list)
    return True


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


# def normalize_fc_count(match_count_dict, recipe_to_fc_count):
#     """Normalizes for a recipe simply having a lot of food compounds"""
#     normalized = match_count_dict.copy()
#     for recipe_id, score in match_count_dict.items():
#         if normalized[recipe_id] > 0:
#             normalized[recipe_id] = normalized[recipe_id] / recipe_to_fc_count
#     return normalized
