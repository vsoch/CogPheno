# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('cognitive_atlas_task', models.CharField(help_text=b"Link to <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a> task", max_length=200, null=True, verbose_name=b'Cognitive Atlas task', blank=True)),
                ('abbreviation', models.CharField(help_text=b'Assessment abbreviation', max_length=250)),
                ('version', models.CharField(help_text=b'version', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contrast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=500)),
                ('label', models.CharField(help_text=b'question unique label', unique=True, max_length=250)),
                ('required', models.BooleanField(default=True, verbose_name=b'Required', choices=[(False, b'Not required'), (True, b'Required')])),
                ('data_type', models.CharField(help_text=b'Data type of the question answer', max_length=200, verbose_name=b'Data Type', choices=[(b'LONGINT', b'Long Integer'), (b'DATETIME', b'Date/Time'), (b'TEXT', b'Text'), (b'INT', b'Integer')])),
                ('assessment', models.ForeignKey(to='assessments.Assessment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numerical_score', models.IntegerField()),
                ('text', models.CharField(max_length=250)),
                ('question', models.ForeignKey(to='assessments.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contrast',
            name='question',
            field=models.ForeignKey(to='assessments.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='concept',
            name='question',
            field=models.ForeignKey(to='assessments.Question'),
            preserve_default=True,
        ),
    ]
