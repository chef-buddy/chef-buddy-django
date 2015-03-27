# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientflavorcompound',
            name='score',
            field=models.FloatField(default=1.0),
            preserve_default=False,
        ),
    ]
