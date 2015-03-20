from django.db import models


class Recipe(models.Model):
    recipe_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return str(self.recipe_id)


class UserFlavorCompound(models.Model):
    user_id = models.IntegerField()
    recipe = models.ForeignKey('Recipe', null=True)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_id)


class IngredientFlavorCompound(models.Model):
    ingredient_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.ingredient_id
