from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pycon.views.home', name='home'),
    # url(r'^pycon/', include('pycon.foo.urls')),
    url(r'^$', 'meetup.views.home'),
    url(r'^add$', 'meetup.views.add'),
    url(r'^robots.txt$', 'meetup.views.robots_txt'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
