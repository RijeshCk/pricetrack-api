# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_productdata_product_previous_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricedetails',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productdata',
            name='product_previous_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productdata',
            name='product_price',
            field=models.FloatField(),
        ),
    ]
