from django.contrib import admin
from chef_buddy.models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    fields = ['recipe_title', 'recipe_image', 'recipe_link']
    search_fields = ['recipe_title']

admin.site.register(Recipe, RecipeAdmin)