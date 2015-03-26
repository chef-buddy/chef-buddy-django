import random
import time
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from chef_buddy.models import UserFlavorCompound
from django.utils.decorators import method_decorator
from chef_buddy.engine import speed_test, get_recipes, get_yummly_recipes, \
    recipes_to_fc_id, store_user_fc, user_to_recipe_counter, \
    store_recipe_fc, recipe_id_to_object, large_image, \
    log_recommendation, get_filtered_recipes, get_curated_random_recipes, user_shown_score


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
    final_rec_result = post_engine(normalized_list[:amount], recipe_id_fc_dict, raw_recipes, user)
    log_recommendation({'user': user,
                        'recipe_id_fc_dict':recipe_id_fc_dict,
                        'normalized_list':normalized_list,
                        'final_rec_result':final_rec_result})
    return Response(final_rec_result)

@api_view(['GET'])
@method_decorator(csrf_exempt)
@speed_test
def recipe_list(request):
    """Returns a list of suggested recipes"""
    amount = 10
    user = request.GET.get('user', 1)
    search = request.GET.get('search', '')
    print("search {}".format(search))
    print("user {}".format(user))
    filters = request.GET.getlist('filter', [])
    print("filters {}".format(filters))
    raw_recipes = get_filtered_recipes(search, filters, amount)
    recipe_id_fc_dict = recipes_to_fc_id(raw_recipes)
    sorted_list = rec_engine(recipe_id_fc_dict, user)
    json_recipes = post_engine(sorted_list[:amount], recipe_id_fc_dict, raw_recipes, user)
    return Response(json_recipes)

@speed_test
def list_pre_engine(user, label_list, amount):
    start = time.time()
    raw_recipes = get_filtered_recipes(label_list, amount)
    end = time.time()
    print('yummly response time ', end-start)
    recipe_id_fc_dict = recipes_to_fc_id(raw_recipes)
    return recipe_id_fc_dict, raw_recipes


@speed_test
def pre_engine(user):
    start = time.time()
    if UserFlavorCompound.objects.filter(user_id=user).count() < 30 or random.random() < .05:
        raw_recipes = get_curated_random_recipes()
    else:
        raw_recipes = get_yummly_recipes()
    end = time.time()
    print('yummly response time ', end-start)

    recipe_id_fc_dict = recipes_to_fc_id(raw_recipes)
    return recipe_id_fc_dict, raw_recipes

@speed_test
def rec_engine(recipe_id_fc_dict, user):
    """recipe_id_fc_dict = dictionary containing the id of the recipe to a list of the food compounds
    user = id of the user that is being predicted for
    This function is the engine for picking a recipe given a user's food compounds.
    Returns a list of recipes in tuple form (recipe_id, score)."""

    unsorted_score_list = user_to_recipe_counter(recipe_id_fc_dict, user)
    scored_list = sorted(unsorted_score_list, key=lambda x: x[1], reverse=True)
    return scored_list

@speed_test
def post_engine(scored_list, recipe_id_fc_dict, raw_recipes, user):
    for recipe_id, score in scored_list:
        store_recipe_fc(recipe_id, recipe_id_fc_dict[recipe_id])
    rec_object_list = []
    for recipe_id, score in scored_list:
        rec_object = recipe_id_to_object(recipe_id, raw_recipes)
        rec_object['recommendation_score'] = user_shown_score(recipe_id_fc_dict[recipe_id], user)
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
