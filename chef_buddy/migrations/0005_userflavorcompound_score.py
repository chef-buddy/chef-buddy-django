# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0004_auto_20150317_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflavorcompound',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
