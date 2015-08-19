# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0008_add_assessment_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cognitiveatlasconcept',
            name='name',
            field=models.CharField(max_length=1000),
            preserve_default=True,
        ),
    ]
