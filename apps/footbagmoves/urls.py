from django.conf.urls import patterns, url

from apps.footbagmoves import views

urlpatterns = patterns('', 
    url(r'^$', views.component_index, name='component_index')
)
