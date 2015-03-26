# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0013_delete_yummlyresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='YummlyResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('recipe_id', models.CharField(max_length=200)),
                ('response', jsonfield.fields.JSONField()),
                ('flavor_id', models.ForeignKey(to='chef_buddy.Recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
