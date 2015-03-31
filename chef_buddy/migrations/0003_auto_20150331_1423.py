# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0002_ingredientflavorcompound_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticIngredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('recipe_num_id', models.CharField(max_length=200)),
                ('ingredient', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaticRecipe',
            fields=[
                ('num_id', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=200)),
                ('recipeName', models.CharField(max_length=300)),
                ('imageUrlsBySize', models.CharField(max_length=300)),
                ('sourceDisplayName', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='staticingredient',
            unique_together=set([('recipe_num_id', 'ingredient')]),
        ),
    ]
