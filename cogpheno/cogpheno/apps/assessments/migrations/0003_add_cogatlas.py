# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_add_cogatlas_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CognitiveAtlasConcept',
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
        migrations.AddField(
            model_name='cognitiveatlasconcept',
            name='task',
            field=models.ForeignKey(to='assessments.CognitiveAtlasTask'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='cognitive_atlas_contrast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Cognitive Atlas Contrast', to='assessments.CognitiveAtlasConcept', help_text=b"Contrast defined in the <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a>", null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assessment',
            name='cognitive_atlas_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Cognitive Atlas Task', to='assessments.CognitiveAtlasTask', help_text=b"Assessment defined in the <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a>", null=True),
            preserve_default=True,
        ),
    ]
