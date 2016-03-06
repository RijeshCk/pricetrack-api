# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160306_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdata',
            name='product_extra_data',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
