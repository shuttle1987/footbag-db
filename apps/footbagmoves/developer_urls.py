"""URL processing for the developers pages"""
from django.conf.urls import url

from apps.footbagmoves import developer_views

urlpatterns = [
    url(r'^$', developer_views.index, name='developer-index'),
    url(r'^index$', developer_views.index, name='developer-index'),
    url(r'^components.json$', developer_views.jsonComponentsView, name='components-json'),
    url(r'^moves.json$', developer_views.jsonMovesView, name='moves-json'),
]
