# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20160306_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdata',
            name='procuct_extra_data',
            field=models.CharField(max_length=10),
        ),
    ]
