# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0005_userflavorcompound_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_image',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_link',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_title',
        ),
        migrations.AddField(
            model_name='recipe',
            name='flavor_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
