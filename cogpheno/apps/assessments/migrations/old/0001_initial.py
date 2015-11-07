# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


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
                ('abbreviation', models.CharField(help_text=b'Assessment abbreviation', max_length=250)),
                ('version', models.CharField(help_text=b'version', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CognitiveAtlasConcept',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('cog_atlas_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('definition', models.CharField(default=None, max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CognitiveAtlasTask',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('cog_atlas_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
            ],
            options={
                'ordering': ['name'],
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
                ('data_type', models.CharField(help_text=b'Data type of the question answer', max_length=200, verbose_name=b'Data Type', choices=[(b'LONGINT', b'Long Integer'), (b'DATETIME', b'Date/Time'), (b'TEXT', b'Text'), (b'INT', b'Integer'), (b'DOUBLE', b'Double')])),
                ('options', models.CharField(default=None, max_length=500)),
                ('assessment', models.ForeignKey(to='assessments.Assessment')),
                ('cognitive_atlas_concept', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Cognitive Atlas Concept', to='assessments.CognitiveAtlasConcept', help_text=b"Concept defined in the <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a>", null=True)),
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
                ('questions', models.ManyToManyField(to='assessments.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='assessment',
            name='cognitive_atlas_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Cognitive Atlas Task', to='assessments.CognitiveAtlasTask', help_text=b"Assessment defined in the <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a>", null=True),
            preserve_default=True,
        ),
    ]
