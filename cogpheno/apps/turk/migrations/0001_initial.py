# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mturk_id', models.CharField(help_text=b'A unique identifier for the assignment', max_length=255, unique=True, null=True, verbose_name=b'Assignment ID')),
                ('worker_id', models.CharField(help_text=b'The ID of the Worker who accepted the HIT', max_length=255, null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=1, null=True, help_text=b'The status of the assignment', choices=[(b'S', b'Submitted'), (b'A', b'Approved'), (b'R', b'Rejected')])),
                ('auto_approval_time', models.DateTimeField(help_text=b'If results have been submitted, this is the date and time, in UTC,  the results of the assignment are considered approved automatically if they have not already been explicitly approved or rejected by the requester', null=True, blank=True)),
                ('accept_time', models.DateTimeField(help_text=b'The date and time, in UTC, the Worker accepted  the assignment', null=True, blank=True)),
                ('submit_time', models.DateTimeField(help_text=b'If the Worker has submitted results, this is the date and time, in UTC, the assignment was submitted', null=True, blank=True)),
                ('approval_time', models.DateTimeField(help_text=b'If requester has approved the results, this is the date and time, in UTC, the results were approved', null=True, blank=True)),
                ('rejection_time', models.DateTimeField(help_text=b'If requester has rejected the results, this is the date and time, in UTC, the results were rejected', null=True, blank=True)),
                ('deadline', models.DateTimeField(help_text=b'The date and time, in UTC, of the deadline for the assignment', null=True, blank=True)),
                ('requester_feedback', models.TextField(help_text=b'The optional text included with the call to either approve or reject the assignment.', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HIT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mturk_id', models.CharField(help_text=b'A unique identifier for the HIT', max_length=255, unique=True, null=True, verbose_name=b'HIT ID')),
                ('hit_type_id', models.CharField(help_text=b'The ID of the HIT type of this HIT', max_length=255, null=True, verbose_name=b'HIT Type ID', blank=True)),
                ('creation_time', models.DateTimeField(help_text=b'The UTC date and time the HIT was created', null=True, blank=True)),
                ('title', models.CharField(help_text=b'The title of the HIT', max_length=255, null=True, blank=True)),
                ('description', models.TextField(help_text=b'A general description of the HIT', null=True, blank=True)),
                ('keywords', models.TextField(help_text=b'One or more words or phrases that describe the HIT, separated by commas.', null=True, verbose_name=b'Keywords', blank=True)),
                ('status', models.CharField(choices=[(b'A', b'Assignable'), (b'U', b'Unassignable'), (b'R', b'Reviewable'), (b'G', b'Reviewing'), (b'D', b'Disposed')], max_length=1, blank=True, help_text=b'The status of the HIT and its assignments', null=True, verbose_name=b'HIT Status')),
                ('reward', models.DecimalField(help_text=b'The amount of money the requester will pay a worker for successfully completing the HIT', null=True, max_digits=5, decimal_places=3, blank=True)),
                ('lifetime_in_seconds', models.PositiveIntegerField(help_text=b'The amount of time, in seconds, after which the HIT is no longer available for users to accept.', null=True, blank=True)),
                ('assignment_duration_in_seconds', models.PositiveIntegerField(help_text=b'The length of time, in seconds, that a worker has to complete the HIT after accepting it.', null=True, blank=True)),
                ('max_assignments', models.PositiveIntegerField(default=1, help_text=b'The number of times the HIT can be accepted and completed before the HIT becomes unavailable.', null=True, blank=True)),
                ('auto_approval_delay_in_seconds', models.PositiveIntegerField(help_text=b'The amount of time, in seconds after the worker submits an assignment for the HIT that the results are automatically approved by the requester.', null=True, blank=True)),
                ('requester_annotation', models.TextField(help_text=b'An arbitrary data field the Requester who created the HIT can use. This field is visible only to the creator of the HIT.', null=True, blank=True)),
                ('number_of_similar_hits', models.PositiveIntegerField(help_text=b'The number of HITs with fields identical to this HIT, other than the Question field.', null=True, blank=True)),
                ('review_status', models.CharField(choices=[(b'N', b'NotReviewed'), (b'M', b'MarkedForReview'), (b'R', b'ReviewedAppropriate'), (b'I', b'ReviewedInappropriate')], max_length=1, blank=True, help_text=b'Indicates the review status of the HIT.', null=True, verbose_name=b'HIT Review Status')),
                ('number_of_assignments_pending', models.PositiveIntegerField(help_text=b'The number of assignments for this HIT that have been accepted by Workers, but have not yet been submitted, returned, abandoned.', null=True, blank=True)),
                ('number_of_assignments_available', models.PositiveIntegerField(help_text=b'The number of assignments for this HIT that are available for Workers to accept', null=True, blank=True)),
                ('number_of_assignments_completed', models.PositiveIntegerField(help_text=b'The number of assignments for this HIT that have been approved or rejected.', null=True, blank=True)),
                ('content_id', models.PositiveIntegerField(help_text=b'Any Django model can be generically attached to this HIT. This is the id of that model instance.', null=True, verbose_name=b'Content id', blank=True)),
                ('content_type', models.ForeignKey(related_name='hit', blank=True, to='contenttypes.ContentType', help_text=b'Any Django model can be generically attached to this HIT. This is the content type of that model instance.', null=True, verbose_name=b'Content type')),
            ],
            options={
                'verbose_name': 'HIT',
                'verbose_name_plural': 'HITs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b'The Key (variable) for a QuestionAnswer', max_length=255)),
                ('value', models.TextField(help_text=b'The value associated with the key', null=True, blank=True)),
                ('assignment', models.ForeignKey(related_name='answers', blank=True, to='turk.Assignment', null=True)),
            ],
            options={
                'verbose_name': 'Key-Value Pair',
                'verbose_name_plural': 'Key-Value Pairs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='assignment',
            name='hit',
            field=models.ForeignKey(related_name='assignments', blank=True, to='turk.HIT', null=True),
            preserve_default=True,
        ),
    ]
