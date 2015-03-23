import requests
import random
import time
from datetime import datetime
from django.db.models import F, Count
from chef_buddy.models import Recipe, UserFlavorCompound, IngredientFlavorCompound
import os

_app_id = os.environ['APP_ID']
_app_key = os.environ['APP_KEY']


def get_recipes(amount):
    random_start = random.randint(1, (321961 - amount))
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes',
                               params={'_app_id':_app_id, '_app_key':_app_key,
                                       'maxResult':amount, 'requirePictures':'true',
                                       'start':random_start })
    return all_recipes.json()


def get_yummly_recipes():
    recipes = get_recipes(10)
    return recipes['matches']


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
        flavor_compounds = IngredientFlavorCompound.objects.filter(ingredient_id__in=ingredients)\
                                                           .values_list('flavor_id', flat=True)
        recipe_fc_dict[recipe] = flavor_compounds
    return recipe_fc_dict


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



def recipe_id_to_object(recipe_id, recipe_list):
    """Looks recipe_id in recipe_list and returns recipe object"""
    for recipe in recipe_list:
        if recipe['id'] == recipe_id:
            return recipe


def user_to_recipe_counter(recipe_id_fc_dict, user):
    """Takes in user's flavor compounds and recipe flavor compounds to produce a list of how
    many times the flavor compounds of the user appear in each recipe for the user. Each time
    a flavor compound appears, the score associated with the user's fc will be added to the recipe"""

    match_list = []
    for recipe_id, fc_id_list in recipe_id_fc_dict.items():
        matched_query = UserFlavorCompound.objects. \
            values('flavor_id'). \
            filter(user_id=user, flavor_id__in=fc_id_list, score__gt=0)
        matched_count = matched_query.count()
        if len(fc_id_list) != 0:
            score = (matched_count / len(fc_id_list) * 100)
        else:
            score = 0
        match_list.append((recipe_id, score))
    return match_list


def large_image(json):
    """
    Takes the image from the Yummly api and returns a larger image by changing the URL.
    :return: json object
    """
    image = json["imageUrlsBySize"]['90']
    json['largeImage'] = image.replace('=s90-c', '=s600')
    return json



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
