# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151122_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdata',
            name='product_previous_price',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
