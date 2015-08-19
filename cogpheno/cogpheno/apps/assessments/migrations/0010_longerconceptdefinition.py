# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0009_longerconceptname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cognitiveatlasconcept',
            name='definition',
            field=models.CharField(default=None, max_length=5000),
            preserve_default=True,
        ),
    ]
