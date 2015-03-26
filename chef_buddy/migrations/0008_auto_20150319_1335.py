# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0007_auto_20150317_2136'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userflavorcompound',
            unique_together=set([('user_id', 'flavor_id')]),
        ),
    ]
