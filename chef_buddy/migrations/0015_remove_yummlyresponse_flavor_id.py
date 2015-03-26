# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0014_yummlyresponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yummlyresponse',
            name='flavor_id',
        ),
    ]
