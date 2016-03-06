# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160306_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdata',
            name='procuct_extra_data',
            field=jsonfield.fields.JSONField(),
        ),
    ]
