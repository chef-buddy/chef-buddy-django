# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0003_auto_20150317_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientflavorcompound',
            name='ingredient_id',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
