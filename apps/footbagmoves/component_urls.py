"""URL processing for footbag components"""
from django.conf.urls import url

from apps.footbagmoves import views

urlpatterns = [
    url(r'^$', views.component_index, name='component_index'),
    url(r'^(?P<component_slug>[\w-]+)/$', views.component_detail, name='component_detail'),
]
