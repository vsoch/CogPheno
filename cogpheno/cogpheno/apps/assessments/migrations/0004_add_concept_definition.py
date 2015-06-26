# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_add_cogatlas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cognitiveatlasconcept',
            name='task',
        ),
        migrations.AddField(
            model_name='cognitiveatlasconcept',
            name='definition',
            field=models.CharField(default=None, max_length=200),
            preserve_default=True,
        ),
    ]
