# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0004_question_direction'),
    ]

    operations = [
        migrations.CreateModel(
            name='BehavioralTrait',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('unique_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('definition', models.CharField(default=None, max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='question',
            name='cognitive_atlas_concept',
        ),
    ]
