"""URL processing for footbag components"""
from django.conf.urls import patterns, url

from apps.footbagmoves import views

urlpatterns = patterns('', 
    url(r'^$', views.component_index, name='component_index'),
    url(r'^(?P<component_name>[\w-]+)/$', views.component_detail, name='component_detail'),
)
