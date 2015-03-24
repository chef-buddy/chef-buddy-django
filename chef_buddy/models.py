from django.db import models
from jsonfield import JSONField


class Recipe(models.Model):
    recipe_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.recipe_id


class UserFlavorCompound(models.Model):
    user_id = models.IntegerField()
    flavor_id = models.IntegerField(null=True)
    score = models.IntegerField()

    class Meta:
        unique_together = ("user_id", "flavor_id")

    def __str__(self):
        return str(self.user_id)


class IngredientFlavorCompound(models.Model):
    ingredient_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.ingredient_id


class YummlyResponse(models.Model):
    recipe_id = models.CharField(max_length=200)
    response = JSONField()

    def __str__(self):
        return self.recipe_id