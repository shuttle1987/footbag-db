from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
from apps.home import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.home.views.index', name='basic_homepage'),#match the bare domain name
    # url(r'^blog/', include('blog.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    url(r'^admin/', include(admin.site.urls)),
)
