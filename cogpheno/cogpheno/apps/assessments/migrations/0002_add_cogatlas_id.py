# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concept',
            name='cognitive_atlas_id',
            field=models.CharField(default=None, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrast',
            name='cognitive_atlas_id',
            field=models.CharField(default=None, max_length=250),
            preserve_default=True,
        ),
    ]
