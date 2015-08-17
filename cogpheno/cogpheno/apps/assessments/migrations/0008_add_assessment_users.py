# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessments', '0007_behavior_trait_synset'),
    ]

    operations = [
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
