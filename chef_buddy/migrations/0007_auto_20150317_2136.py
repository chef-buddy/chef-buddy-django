# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0006_auto_20150317_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_id',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
