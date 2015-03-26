from django.contrib import admin
from chef_buddy.models import Recipe, UserFlavorCompound, IngredientFlavorCompound, YummlyResponse

class RecipeAdmin(admin.ModelAdmin):
    fields = ['recipe_id', 'flavor_id']
    search_fields = ['recipe_id']
    list_display = ('recipe_id', 'flavor_id')

class IngredientFlavorCompoundAdmin(admin.ModelAdmin):
    fields = ['ingredient_id', 'flavor_id']
    list_display = ('ingredient_id', 'flavor_id')
    search_fields = ['ingredient_id']

class UserFlavorCompoundAdmin(admin.ModelAdmin):
    fields = ['id', 'user_id', 'flavor_id', 'score']
    list_display = ('user_id', 'flavor_id', 'score')
    search_fields = ['user_id']

class YummlyResponseAdmin(admin.ModelAdmin):
    fields = ['recipe_id', 'response']
    search_fields = ['response']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientFlavorCompound, IngredientFlavorCompoundAdmin)
admin.site.register(UserFlavorCompound, UserFlavorCompoundAdmin)
admin.site.register(YummlyResponse, YummlyResponseAdmin)