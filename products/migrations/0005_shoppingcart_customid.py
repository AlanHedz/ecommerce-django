# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='customid',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
    ]
