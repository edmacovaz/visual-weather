from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'visual_weather.views.index', name='home'),
    url(r'^(\d{4}-\d{2}-\d{2})/(.*)/(.*)/$', 'visual_weather.views.for_day', name='for_day'),
    #url(r'^visual_weather/', include('visual_weather.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
