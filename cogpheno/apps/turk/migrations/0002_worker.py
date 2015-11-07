# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_question_flagged_for_curation'),
        ('turk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('worker_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('questions', models.ManyToManyField(related_query_name=b'questions', related_name='questions_answered', to='assessments.Question', blank=True, help_text=b'These are questions that have been granted to a worker.', verbose_name=b'Worker questions')),
            ],
            options={
                'ordering': ['worker_id'],
            },
            bases=(models.Model,),
        ),
    ]
