# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0002_recipeflavorcompound_userflavorcompound'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeFlavorCompound',
            new_name='IngredientFlavorCompound',
        ),
        migrations.RenameField(
            model_name='ingredientflavorcompound',
            old_name='user_id',
            new_name='ingredient_id',
        ),
    ]
