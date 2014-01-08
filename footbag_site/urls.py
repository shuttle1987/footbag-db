from django.conf.urls import patterns, include, url

from django.contrib import admin
from apps.home import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.home.views.index', name='basic_homepage'),#match the bare domain name
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
