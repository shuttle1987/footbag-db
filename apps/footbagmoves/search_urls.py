"""URL processing for the search functionality """
from django.conf.urls import url

from apps.footbagmoves import views

urlpatterns = [
    url(r'^$', views.search_page, name='search'),
]
