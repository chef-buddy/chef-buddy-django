from tastypie.resources import ModelResource
from chef_buddy.models import Recipe


class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        resource_name = 'recipe'