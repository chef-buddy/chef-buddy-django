# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0003_auto_20150331_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staticingredient',
            old_name='recipe_num_id',
            new_name='recipe_id',
        ),
        migrations.AlterUniqueTogether(
            name='staticingredient',
            unique_together=set([('recipe_id', 'ingredient')]),
        ),
    ]
