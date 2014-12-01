"""URL processing for editing footbag moves and components"""
from django.conf.urls import patterns, url

from apps.footbagmoves import edit_views

urlpatterns = patterns('', 
    #url(r'^$', views.edit_index, name='edit_index'),
    url(r'^component/$', edit_views.component_new, name='component-new'),
    url(r'^component/(?P<component_id>\d+)/$', edit_views.component_modify, name='component-edit'),
    url(r'^move/$', edit_views.move_new, name='move-new'),
    url(r'^move/(?P<move_id>\d+)/$', edit_views.move_modify, name='move-edit'),
)
