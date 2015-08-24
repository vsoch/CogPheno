# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='behavioraltrait',
            name='pos',
            field=models.CharField(default=None, max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
