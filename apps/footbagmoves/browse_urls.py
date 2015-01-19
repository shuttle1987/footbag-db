"""URL processing for the move and components browse page"""
from django.conf.urls import patterns, url

from apps.footbagmoves import browse_views

urlpatterns = patterns(
    '',
    url(r'^components/$', browse_views.ComponentList.as_view(), name='component-list'),
    url(r'^moves/$', browse_views.MoveList.as_view(), name='move-list'),
)
