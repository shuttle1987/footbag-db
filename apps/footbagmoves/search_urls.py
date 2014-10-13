"""URL processing for the search functionality """
from django.conf.urls import patterns, url

from apps.footbagmoves import views

urlpatterns = patterns('', 
    url(r'^$', views.search_page, name='search'),
)
