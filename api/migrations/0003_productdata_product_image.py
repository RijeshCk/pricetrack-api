# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_productdata_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdata',
            name='product_image',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
