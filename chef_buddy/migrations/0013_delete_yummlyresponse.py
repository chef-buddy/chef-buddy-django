# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0012_auto_20150322_2111'),
    ]

    operations = [
        migrations.DeleteModel(
            name='YummlyResponse',
        ),
    ]
