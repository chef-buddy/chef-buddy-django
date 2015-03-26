# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0008_auto_20150319_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflavorcompound',
            name='liked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userflavorcompound',
            name='recipe',
            field=models.ForeignKey(null=True, to='chef_buddy.Recipe'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='userflavorcompound',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='userflavorcompound',
            name='score',
        ),
        migrations.RemoveField(
            model_name='userflavorcompound',
            name='flavor_id',
        ),
    ]
