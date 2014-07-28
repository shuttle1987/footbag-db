"""URL processing for footbag moves"""
from django.conf.urls import patterns, url

from apps.footbagmoves import views

urlpatterns = patterns('', 
    url(r'^$', views.move_index, name='move_index'),
    url(r'^(?P<move_slug>[\w-]+)/$', views.move_detail, name='move_detail'),
)
