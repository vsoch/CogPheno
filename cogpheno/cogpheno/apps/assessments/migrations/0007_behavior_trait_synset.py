# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0006_question_behavioral_trait'),
    ]

    operations = [
        migrations.AddField(
            model_name='behavioraltrait',
            name='wordnet_synset',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='behavioraltrait',
            name='definition',
            field=models.CharField(default=None, max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
