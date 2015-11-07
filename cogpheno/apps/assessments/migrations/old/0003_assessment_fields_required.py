# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_options_can_be_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='abbreviation',
            field=models.CharField(default=None, max_length=250, null=True, help_text=b'Assessment abbreviation', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assessment',
            name='version',
            field=models.CharField(help_text=b'version', max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
