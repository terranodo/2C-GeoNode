
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import h_keywords

from geonode.urls import *

urlpatterns = patterns('',
    url(r'^/?$',TemplateView.as_view(template_name='site_index.html'),name='home'),
    url(r'^h_keywords_api$', h_keywords, name='h_keywords_api'),
 ) + urlpatterns
