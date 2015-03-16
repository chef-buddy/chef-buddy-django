# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_buddy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeFlavorCompound',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_id', models.IntegerField()),
                ('flavor_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserFlavorCompound',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_id', models.IntegerField()),
                ('flavor_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
