from django.db import models
from jsonfield import JSONField


class Recipe(models.Model):
    recipe_id = models.CharField(max_length=200)
    flavor_id = models.IntegerField()

    def __str__(self):
        return self.recipe_id


class UserFlavorCompound(models.Model):
    user_id = models.IntegerField(db_index=True)
    flavor_id = models.IntegerField(null=True)
    score = models.IntegerField()

    class Meta:
        unique_together = ("user_id", "flavor_id")

    def __str__(self):
        return str(self.user_id)


class IngredientFlavorCompound(models.Model):
    ingredient_id = models.CharField(max_length=200, db_index=True)
    flavor_id = models.IntegerField()
    score = models.FloatField()

    def __str__(self):
        return self.ingredient_id


class YummlyResponse(models.Model):
    recipe_id = models.CharField(max_length=200)
    response = JSONField()

    def __str__(self):
        return self.recipe_id


class StaticRecipe(models.Model):
    num_id = models.AutoField()
    id = models.CharField(max_length=200, primary_key=True)
    recipeName = models.CharField(max_length=300)
    imageUrlsBySize = models.CharField(max_length=300)
    sourceDisplayName = models.CharField(max_length=200)

    def __str__(self):
        return self.recipe_id


class StaticIngredient(models.Model):
    recipe_id = models.CharField(max_length=200)
    ingredient = models.CharField(max_length=200)

    class Meta:
        unique_together = ("recipe_id", "ingredient")

    def __str__(self):
        return self.ingredient
