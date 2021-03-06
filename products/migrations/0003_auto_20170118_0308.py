# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 03:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_shoppingcart'),
    ]

    operations = [
        migrations.CreateModel(
            name='InShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('shopping_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ShoppingCart')),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='products',
            field=models.ManyToManyField(through='products.InShoppingCart', to='products.Product'),
        ),
    ]
