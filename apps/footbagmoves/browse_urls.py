"""URL processing for the move and components browse page"""
from django.conf.urls import url

from apps.footbagmoves import browse_views

urlpatterns = [
    url(r'^components/$', browse_views.ComponentList.as_view(), name='component-list'),
    url(r'^moves/$', browse_views.MoveList.as_view(), name='move-list'),
]
