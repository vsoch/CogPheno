# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.CharField(default=None, max_length=500, null=True),
            preserve_default=True,
        ),
    ]
