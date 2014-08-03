""" This handles the top level URL routing for the site
"""
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
from apps.home import views
from apps.footbagmoves import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'apps.home.views.index', name='basic_homepage'),#match the bare domain name
    #url(r'^about.html', 'apps.home.views.about', name='about_page'),#match the about page
    url(r'^about$', TemplateView.as_view(template_name='home/about.html'), name='about'),
    #url(r'^components/', include('apps.footbagmoves.urls', namespace='footbagmoves')),#namespace currently causing issues with url reverse matching in components index
    url(r'^components/', include('apps.footbagmoves.urls')),
    url(r'^moves/', include('apps.footbagmoves.move_urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='home/robots.txt', content_type='text/plain'), name='robots'),
    url(r'^admin/', include(admin.site.urls)),
)
