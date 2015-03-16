import random
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from chef_buddy.models import Recipe
from chef_buddy_django.urls import RecipeSerializer

# Create your views here.

@api_view(['GET'])
def get_random_recipe(request):
    if request.method == 'GET':
        random_idx = random.randint(0, Recipe.objects.count() - 1)
        recipe = Recipe.objects.all()[random_idx]
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)
