# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0005_remove_cogat_concept'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='behavioral_trait',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Behavioral Trait', to='assessments.BehavioralTrait', help_text=b'Behavioral trait described by the question', null=True),
            preserve_default=True,
        ),
    ]
