from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'market.views.home', name='home'),
    url(r'^learn-more/$', TemplateView.as_view(template_name="learn-more.html")),
    # url(r'^market/', include('market.foo.urls')),

    url(r'^register/$', 'market.views.register', name='register'),
    url(r'^account/login/$', 'market.views.loginview', name='login'),
    url(r'^account/logout/$', 'market.views.logoutview', name='logout'),

    url(r'^app/', include('market.apps.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # dependencies
    (r'^search/', include('haystack.urls')),
)
