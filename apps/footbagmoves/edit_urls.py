"""URL processing for editing footbag moves and components"""
from django.conf.urls import patterns, url

from apps.footbagmoves import edit_views

urlpatterns = patterns('', 
    #url(r'^$', views.edit_index, name='edit_index'),
    url(r'^component/$', edit_views.component_edit, name='component_edit'),
    url(r'^component/(?P<component_id>[0-9]+)/$', edit_views.component_edit, name='component_edit'),
    #url(r'^move/(?P<move_id>[0-9]+)/$', views.move_edit, name='move_edit'),
)
