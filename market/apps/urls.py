from django.conf.urls import patterns, include, url
from market.apps import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'market.views.home', name='home'),
    # url(r'^market/', include('market.foo.urls')),
    url(r'^id/([0-9 ]+)/$', views.app, name="app"),
    url(r'^list/latest/$', views.LatestView.as_view(), name="apps_latest"),
    url(r'^list/category/([a-zA-Z]+)/$', views.CategoryView.as_view(), name="apps_category"),
    url(r'^browse/$', TemplateView.as_view(template_name="apps/browse.html"), name="apps_browse"),
    url(r'^submit/$', views.submitview, name="apps_submit"),
)
