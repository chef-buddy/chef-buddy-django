from django.db import models


class Recipe(models.Model):
    recipe_id = models.IntegerField()
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.recipe_id


class UserFlavorCompound(models.Model):
    user_id = models.IntegerField()
    flavor_id = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return self.user_id


class IngredientFlavorCompound(models.Model):
    ingredient_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.ingredient_id
