from .views import assessments_view, questions_view, behaviors_view, edit_assessment, edit_question, view_assessment, view_question, delete_assessment, delete_question, edit_questions, export_questions, export_questions, export_assessment, add_concept, delete_question_redirect, view_behavior, delete_behavior, edit_behavior, view_behavior_question
from django.views.generic.base import TemplateView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Assessments
    url(r'^assessments$', assessments_view, name="assessments"),
    url(r'^questions$', questions_view, name="questions"),
    url(r'^behaviors$', behaviors_view, name="behaviors"),
    url(r'^behaviors/(?P<bid>.*)/$',view_behavior, name='behavior_details'),
    url(r'^behaviors/(?P<bid>.*)/delete$',delete_behavior,name='delete_behavior'),
    url(r'^behaviors/(?P<bid>.*)/edit_behavior$',edit_behavior,name='edit_behavior'),
    url(r'^assessments/new$',edit_assessment,name='new_assessment'),
    url(r'^assessments/(?P<aid>\d+|[A-Z]{8})/new$',edit_assessment,name='new_assessment'),
    url(r'^questions/(?P<qid>\d+|[A-Z]{8})/behavior$',view_behavior_question,name='view_behavior_question'),
    url(r'^questions/(?P<qid>\d+|[A-Z]{8})/edit$',edit_question,name='edit_question'),
    url(r'^assessments/(?P<aid>\d+|[A-Z]{8})/$',view_assessment, name='assessment_details'),
    url(r'^questions/(?P<qid>\d+|[A-Z]{8})/$',view_question, name='question_details'),
    url(r'^concepts/(?P<qid>\d+|[A-Z]{8})/add/$',add_concept, name='add_concept'),
    url(r'^assessments/(?P<aid>\d+|[A-Z]{8})/delete$',delete_assessment,name='delete_assessment'),
    url(r'^assessments/(?P<aid>\d+|[A-Z]{8})/export$',export_assessment,name='export_assessment'),
    url(r'^questions/export$',export_questions,name='export_questions'),
    url(r'^questions/(?P<qid>\d+|[A-Z]{8})/delete$',delete_question,name='delete_question'),
    url(r'^questions/(?P<qid>\d+|[A-Z]{8})/deleteredirect$',delete_question_redirect,name='delete_question_redirect'),
    url(r'^assessments/(?P<assessment_aid>\d+|[A-Z]{8})/edit$',edit_questions,name="edit_questions"),

)
