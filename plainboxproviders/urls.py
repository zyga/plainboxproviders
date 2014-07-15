from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from providerfrontend.views import Home

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    # Examples:
    # url(r'^$', 'plainboxproviders.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
