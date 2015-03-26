import random
import requests
import os
from .models import IngredientFlavorCompound, UserFlavorCompound, YummlyResponse, Recipe


_app_id = '2c2e3eb7'
_app_key = 'ba0ff4337064f14cfedeb994e8a639d2'


class YummlyRecipe:
    def __init__(self, recipe_id, response, flavor_compounds):
        self.name = recipe_id
        self.response = response
        self.flavor_compounds = flavor_compounds


def scrape_yummly():
    recipes = get_yummly_recipes()
    recipe_list = recipe_objects(recipes)
    for recipe in recipe_list:
        Y = YummlyResponse(recipe_id=recipe.name, response=recipe.response)
        Y.save()
        for flavor in recipe.flavor_compounds:
            r = Recipe(recipe_id=recipe.name, flavor_id=flavor)
            r.save()


def get_yummly_recipes(amount=20):
    recipes = get_recipes(amount)
    return recipes['matches']


def get_recipes(amount):
    random_start = random.randint(1, (321961 - amount))
    all_recipes = requests.get('http://api.yummly.com/v1/api/recipes',
                               params={'_app_id':_app_id, '_app_key':_app_key,
                                       'maxResult':amount, 'requirePictures':'true',
                                       'start':random_start })
    return all_recipes.json()


def recipe_objects(recipe_list):
    """recipe_list = raw list of recipes directly from yummly
    takes in a list of recipes and returns a dict of recipe_id, [ingredients]"""
    recipe_obj_list = []
    for recipe in recipe_list:
        ingredients = [ingredient for ingredient in recipe['ingredients']]
        flavor_compounds = IngredientFlavorCompound.objects.filter(ingredient_id__in=ingredients)\
                                                           .values_list('flavor_id', flat=True)
        response = recipe
        name = recipe['id']
        recipe = YummlyRecipe(name, response, flavor_compounds)
        recipe_obj_list.append(recipe)
    return recipe_obj_list