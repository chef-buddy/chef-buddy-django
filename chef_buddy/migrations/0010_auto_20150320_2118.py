# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0009_auto_20150320_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflavorcompound',
            name='flavor_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userflavorcompound',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='userflavorcompound',
            unique_together=set([('user_id', 'flavor_id')]),
        ),
        migrations.RemoveField(
            model_name='userflavorcompound',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='userflavorcompound',
            name='liked',
        ),
    ]
