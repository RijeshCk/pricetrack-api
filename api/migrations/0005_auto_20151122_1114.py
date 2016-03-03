# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_customauth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customauth',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customauth',
            name='user_description',
        ),
        migrations.AddField(
            model_name='customauth',
            name='access_token',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
