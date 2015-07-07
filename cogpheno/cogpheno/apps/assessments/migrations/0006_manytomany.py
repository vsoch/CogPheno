# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0005_update_concept_definition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concept',
            name='question',
        ),
        migrations.RemoveField(
            model_name='contrast',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionoption',
            name='question',
        ),
        migrations.AddField(
            model_name='concept',
            name='questions',
            field=models.ManyToManyField(to='assessments.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrast',
            name='questions',
            field=models.ManyToManyField(to='assessments.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionoption',
            name='questions',
            field=models.ManyToManyField(to='assessments.Question'),
            preserve_default=True,
        ),
    ]
