from django.contrib import admin
from chef_buddy.models import Recipe, IngredientFlavorCompound

class RecipeAdmin(admin.ModelAdmin):
    fields = ['recipe_title', 'recipe_image', 'recipe_link']
    search_fields = ['recipe_title']

class IngredientFlavorCompoundAdmin(admin.ModelAdmin):
    fields = ['ingredient_id', 'flavor_id']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientFlavorCompound, IngredientFlavorCompoundAdmin)