# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('abbreviation', models.CharField(default=None, max_length=250, null=True, help_text=b'Assessment abbreviation', blank=True)),
                ('version', models.CharField(help_text=b'version', max_length=10, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BehavioralTrait',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('unique_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('definition', models.CharField(default=None, max_length=1000, null=True, blank=True)),
                ('wordnet_synset', models.CharField(default=None, max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CognitiveAtlasConcept',
            fields=[
                ('name', models.CharField(max_length=1000)),
                ('cog_atlas_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('definition', models.CharField(default=None, max_length=5000)),
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
                ('direction', models.CharField(default=b'positive', max_length=10, verbose_name=b'Directionality', choices=[(b'positive', b'Positive (same direction)'), (b'negative', b'Negative (inverse relationship)')])),
                ('data_type', models.CharField(help_text=b'Data type of the question answer', max_length=200, verbose_name=b'Data Type', choices=[(b'LONGINT', b'Long Integer'), (b'DATETIME', b'Date/Time'), (b'TEXT', b'Text'), (b'INT', b'Integer'), (b'DOUBLE', b'Double')])),
                ('options', models.CharField(default=None, max_length=500, null=True)),
                ('assessment', models.ForeignKey(to='assessments.Assessment')),
                ('behavioral_trait', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Behavioral Trait', to='assessments.BehavioralTrait', help_text=b'Behavioral trait described by the question', null=True)),
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
        migrations.AddField(
            model_name='assessment',
            name='contributors',
            field=models.ManyToManyField(related_query_name=b'contributor', related_name='assessment_contributors', to=settings.AUTH_USER_MODEL, blank=True, help_text=b'Select other CogatPheno users to add as contributes to the assessment.  Contributors can add, edit and delete questions in the assessment.', verbose_name=b'Contributors'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assessment',
            name='owner',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
