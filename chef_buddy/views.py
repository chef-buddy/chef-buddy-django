import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from multiprocessing import Pool
from chef_buddy.engine import speed_test, get_recipes, get_yummly_recipes, \
    recipes_to_fc_id, store_user_fc, user_to_recipe_counter, \
    store_recipe_fc, recipe_id_to_object, large_image, log_recommendation


@api_view(['GET', 'POST'])
@method_decorator(csrf_exempt)
@speed_test
def show_top_recipe(request):
    """Manages actual top recipe request process"""
    amount = 1
    post = request.POST.copy()
    user, liked, recipe = post.get('user', 1), post.get('liked', 0), post.get('recipe', '')
    store_user_fc(user, recipe, liked)
    recipe_id_fc_dict, raw_recipes = pre_engine(user)
    normalized_list = rec_engine(recipe_id_fc_dict, user)
    final_rec_result = post_engine(normalized_list[:amount], recipe_id_fc_dict, raw_recipes)
    # log_recommendation({'user': user,
    #                     'recipe_id_fc_dict':recipe_id_fc_dict,
    #                     'normalized_list':normalized_list,
    #                     'final_rec_result':final_rec_result})
    return Response(final_rec_result)

@api_view(['GET', 'POST'])
@method_decorator(csrf_exempt)
@speed_test
def recipe_list(request):
    """Returns a list of suggested recipes"""
    #John change this amount based on how many recipes you want back from the engine
    amount = 1
    post = request.POST.copy()
    user = post.get('user', 1)
    recipe_id_fc_dict, raw_recipes = pre_engine(user)
    sorted_list = rec_engine(recipe_id_fc_dict, user)
    final_rec_result = post_engine(scored_list[:amount], recipe_id_fc_dict, raw_recipes)
    return Response(final_rec_result)

@speed_test
def pre_engine(user):
    raw_recipes = get_yummly_recipes()
    recipe_id_fc_dict = recipes_to_fc_id(raw_recipes)
    return recipe_id_fc_dict, raw_recipes

@speed_test
def rec_engine(recipe_id_fc_dict, user):
    """raw_recipes = list of raw recipes from yummly
    user_fc_dict = user to food compound dict
    amount = how many recipes to return
    This function is the engine for picking a recipe given a user's food compounds.
    Returns recipe object(s)."""

    unsorted_score_list = user_to_recipe_counter(recipe_id_fc_dict, user)
    scored_list = sorted(unsorted_score_list, key=lambda x: x[1], reverse=True)
    return scored_list

@speed_test
def post_engine(scored_list, recipe_id_fc_dict, raw_recipes):
    [store_recipe_fc(recipe_id, recipe_id_fc_dict[recipe_id]) for recipe_id, score in scored_list]
    rec_object_list = []
    for recipe_id, score in scored_list:
        rec_object = recipe_id_to_object(recipe_id, raw_recipes)
        rec_object['recommendation_score'] = score
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
