import requests
import random
import time
import after_response
from datetime import datetime
from django.db.models import F, Count
from chef_buddy.models import Recipe, UserFlavorCompound, IngredientFlavorCompound
import os

_app_id = os.environ['APP_ID']
_app_key = os.environ['APP_KEY']


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


def get_recipes(amount):
    random_start = random.randint(1, (321961 - amount))
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes',
                                params={'_app_id':_app_id, '_app_key':_app_key,
                                        'maxResult':amount, 'requirePictures':'true',
                                        'start':random_start })
    return all_recipes.json()

@speed_test
def get_filtered_recipes(search, label_list, amount):
    params = get_parameters(search, label_list, amount)
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes', params=params)
    recipes = all_recipes.json()
    return recipes['matches']

@speed_test
def get_parameters(search, label_list, amount):
    """Takes in a list of dietary labels and then returns a parameter list to be sent to the yummly api"""
    query = search.replace(' ', '+')
    start = random.randint(1, 2000)
    if query:
        start = 1
    params = {'_app_id':_app_id, '_app_key':_app_key,
              'maxResult': amount, 'requirePictures':'true',
              'allowedDiet[]':[], 'allowedAllergy[]':[],
              'q':query, 'start':start}

    allergy_dict = {'dairy': '396^Dairy-Free', 'egg': '397^Egg-Free',
                    'gluten': '393^Gluten-Free', 'peanut': '394^Peanut-Free',
                    'seafood': '398^Seafood-Free', 'seasame': '399^Sesame-Free',
                    'soy': '400^Soy-Free', 'sulfite': '401^Sulfite-Free',
                    'nut': '395^Tree+Nut-Free', 'wheat': '392^Wheat-Free'}

    diet_dict = {'lacto': '388^Lacto vegetarian', 'ovo': '389^Ovo+vegetarian',
                 'pescetarian': '390^Pescetarian','vegan': '386^Vegan',
                 'vegetarian': '387^Lacto-ovo+vegetarian', 'paleo': '403^Paleo'}
    for label in label_list:
        if label in diet_dict:
            params['allowedDiet[]'].append(diet_dict[label])
        if label in allergy_dict:
            params['allowedAllergy[]'].append(allergy_dict[label])
    return params


def get_yummly_recipes():
    recipes = get_recipes(40)
    return recipes['matches']


def get_curated_random_recipes():
    category_list = ['chicken', 'beef', 'bread', 'tomato', 'cake', 'tuna', 'strawberry',
                     'mexican', 'italian', 'chinese', 'seafood', 'potato', 'cheese']
    params={'_app_id':_app_id, '_app_key':_app_key,
            'maxResult': 40, 'requirePictures':'true',
            'q':random.choice(category_list),
            'start':random.randint(1, 500)}
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes', params=params)
    recipes = all_recipes.json()
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
    Takes in a list of recipes and returns a dict of recipe_id to flavor compound id"""
    recipe_ingr_dict = recipe_ingr_parse(recipe_list)
    recipe_fc_dict = {}
    for recipe, ingredients in recipe_ingr_dict.items():
        recipe_fc_dict[recipe] = IngredientFlavorCompound.objects.filter(ingredient_id__in=ingredients)\
                                                                 .values_list('flavor_id', 'score')
    return recipe_fc_dict


@after_response.enable
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
        UserFlavorCompound.objects.filter(user_id=user_id, flavor_id__in=exists). \
                                   update(score=F('score') + taste)
        new_fc = [num for num in set(flavor_compounds) if num not in set(exists)]
        UserFlavorCompound.objects.bulk_create([UserFlavorCompound(user_id=user_id,flavor_id=flavor,
                                                                   score=taste) for flavor in new_fc])
    return True


def recipe_id_to_object(recipe_id, recipe_list):
    """Looks recipe_id in recipe_list and returns recipe object"""
    for recipe in recipe_list:
        if recipe['id'] == recipe_id:
            return recipe


def user_to_recipe_counter(recipe_id_dict, user):
    """Takes in user's flavor compounds and recipe flavor compounds to produce a list of how
    many times the flavor compounds of the user appear in each recipe for the user. Each time
    a flavor compound appears, the score associated with the user's fc will be added to the recipe"""
    user = int(user)
    match_list = []
    for recipe_id, fc_score_list in recipe_id_dict.items():
        if len(fc_score_list) > 0:
            adj_scores, fc_list = in_common_fc_lookup(user, fc_score_list)
            all_user_fc = UserFlavorCompound.objects.filter(user_id=user).values_list('score', flat=True)
            score = calculate_recipe_score(fc_list, adj_scores, all_user_fc)
        else:
            score = 0
        match_list.append((recipe_id, score))
    return match_list


def in_common_fc_lookup(user, fc_score_list):
    fc_list = [x[0] for x in fc_score_list]
    in_common = dict(UserFlavorCompound.objects.values_list('flavor_id', 'score'). \
                                                filter(user_id=user, flavor_id__in=list(fc_list)))
    adjusted_score_list = [(in_common[fc_id]*score) for fc_id, score in fc_score_list if fc_id in in_common.keys()]
    return adjusted_score_list, fc_list


def calculate_recipe_score(recipe_fc_list, user_fc_scores, all_user_fc):
    total_fc_score = sum([abs(fc) for fc in all_user_fc])
    normalized_scoring = [(fc/total_fc_score) for fc in user_fc_scores]
    engine_score = (sum(normalized_scoring) / len(recipe_fc_list))
    return engine_score


def user_shown_score(recipe_fc_list, user):
    recipe_fc_list = [x[0] for x in recipe_fc_list]
    in_common_fc_score = UserFlavorCompound.objects. \
                         filter(user_id=user, score__gt=1, flavor_id__in=list(recipe_fc_list)). \
                         values_list('flavor_id')
    all_user_fc = UserFlavorCompound.objects.filter(user_id=user).values_list('flavor_id')
    if (len(all_user_fc) < 40):
        return '?'
    else:
        user_score = (len(in_common_fc_score) / len(recipe_fc_list)) * 100
        return round_float(user_score)


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
        recipe_list = [Recipe(recipe_id=str(recipe_id), flavor_id=int(fc_id)) for fc_id, score in flavor_compounds]
        Recipe.objects.bulk_create(recipe_list)
    return True


@after_response.enable
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


def round_float(float):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    y = round(float) - .5
    return int(y) + (y > 0)
