# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=200, blank=True)),
                ('product_price', models.CharField(max_length=10)),
                ('product_url', models.URLField()),
                ('product_id', models.CharField(unique=True, max_length=200)),
                ('procuct_extra_data', models.TextField()),
                ('product_availability', models.CharField(max_length=50)),
                ('product_image', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50)),
                ('product', models.ForeignKey(to='api.ProductData')),
            ],
        ),
        migrations.AddField(
            model_name='pricedetails',
            name='product',
            field=models.ForeignKey(to='api.ProductData'),
        ),
    ]
