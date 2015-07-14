# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_assessment_fields_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='direction',
            field=models.CharField(default=b'positive', max_length=10, verbose_name=b'Directionality', choices=[(b'positive', b'Positive (same direction)'), (b'negative', b'Negative (inverse relationship)')]),
            preserve_default=True,
        ),
    ]
