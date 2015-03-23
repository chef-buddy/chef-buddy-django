import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from multiprocessing import Pool
from chef_buddy.engine import speed_test, get_recipes, get_yummly_recipes, \
    recipes_to_fc_id, store_user_fc, find_user_fc_ids, user_to_recipe_counter, \
    normalize_fc_count, store_recipe_fc, recipe_id_to_object, large_image, \
    score_recommendation



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
    normalized_list = rec_engine(recipe_id_fc_dict, user_fc_dict, 10)
    final_rec_result = post_engine(normalized_list, recipe_id_fc_dict, raw_recipes, user_fc_dict)
    print(len(final_rec_result))
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
@method_decorator(csrf_exempt)
def random_recipe(request):
    recipe_list = get_yummly_recipes()
    recipe = recipe_list[random.randint(1, 10)]
    recipe = large_image(recipe)
    return Response(recipe)
