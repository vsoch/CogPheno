# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_behavioraltrait_pos'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='flagged_for_curation',
            field=models.BooleanField(default=True, verbose_name=b'Flagged for curation in with Amazon Mechanical Turk', choices=[(True, b'Curate'), (False, b"Don't Curate")]),
            preserve_default=True,
        ),
    ]
