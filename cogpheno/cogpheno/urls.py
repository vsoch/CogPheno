from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.http import Http404, HttpResponse
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
import os

from django import template
template.add_to_builtins('django.templatetags.future')
template.add_to_builtins('django.contrib.staticfiles.templatetags.staticfiles')

urlpatterns = patterns('',
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       url(r'^', include('cogpheno.apps.main.urls')),
                       url(r'^', include('cogpheno.apps.assessments.urls')),
                       url(r'^accounts/', include('cogpheno.apps.users.urls')),
                       url(r'^admin/', include(admin.site.urls)))

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>favicon\.ico)$', 'django.views.static.serve', {
            'document_root': os.path.join(settings.STATIC_ROOT,'images')}),
    )
