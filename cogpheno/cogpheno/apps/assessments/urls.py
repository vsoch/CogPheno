from .views import assessments_view, questions_view
from django.views.generic.base import TemplateView
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^assessments', assessments_view, name="assessments"),
    url(r'^questions', questions_view, name="questions"),
)
