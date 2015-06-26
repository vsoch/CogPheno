# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0004_add_concept_definition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='cognitive_atlas_contrast',
        ),
        migrations.AddField(
            model_name='question',
            name='cognitive_atlas_concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Cognitive Atlas Concept', to='assessments.CognitiveAtlasConcept', help_text=b"Concept defined in the <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a>", null=True),
            preserve_default=True,
        ),
    ]
