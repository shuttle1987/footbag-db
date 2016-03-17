""" This handles the top level URL routing for the site
"""
from django.conf.urls import patterns, include, url
from django.conf.urls import (
    handler403,
    handler404,
    handler500,
)

from django.contrib import admin
from django.views.generic import TemplateView

import apps.home.views as homepage
from apps.footbagmoves import views
import user_accounts
from .views import user_panel

urlpatterns = [
    url(r'^$', homepage.index, name='basic_homepage'),#match the bare domain name
    url(r'^about$', TemplateView.as_view(template_name='home/about.html'), name='about'),
    url(r'^components/', include('apps.footbagmoves.component_urls')),
    url(r'^moves/', include('apps.footbagmoves.move_urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^search/', include('apps.footbagmoves.search_urls')),
    url(r'^browse/', include('apps.footbagmoves.browse_urls')),
    url(r'^edit/', include('apps.footbagmoves.edit_urls')),
    url(r'^developers/', include('apps.footbagmoves.developer_urls')),
    url(r'^user_panel/$', user_panel, name='user_panel'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='home/robots.txt', content_type='text/plain'), name='robots'),
#    url(r"^account/signup/$", user_accounts.views.SignupView.as_view(), name="account_signup"),
    url(r'^account/', include('account.urls')),#django-user-accounts
    url(r'^admin/', include(admin.site.urls)),
]

handler403 = 'footbag_site.views.error403'
handler404 = 'footbag_site.views.error404'
handler500 = 'footbag_site.views.error500'
