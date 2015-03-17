from django.db import models


class Recipe(models.Model):
    recipe_title = models.CharField(max_length=200)
    recipe_link = models.CharField(max_length=300)
    recipe_image = models.CharField(max_length=300)

    def __str__(self):
        return self.recipe_title


class UserFlavorCompound(models.Model):
    user_id = models.IntegerField()
    flavor_id = models.IntegerField()
    score = models.IntegerField()


class IngredientFlavorCompound(models.Model):
    ingredient_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.ingredient_id