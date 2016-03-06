# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160306_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productdata',
            old_name='procuct_extra_data',
            new_name='product_extra_data',
        ),
    ]
