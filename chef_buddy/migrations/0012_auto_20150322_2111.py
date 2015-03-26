# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0011_yummlyresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='yummlyresponse',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='yummlyresponse',
            name='user_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
