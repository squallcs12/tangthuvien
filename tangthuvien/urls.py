from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tangthuvien.views.home', name='home'),
    # url(r'^tangthuvien/', include('tangthuvien.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #zinnia
    url(r'^', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

from tangthuvien import settings
if settings.DEBUG:
    urlpatterns += patterns('', (r'^media/(?P<path>.*\.(css|js|jpg|png|gif|bmp|avi|mp3|mp4|wav|pdf|))$', 'django.views.static.serve',
        {'document_root': settings.realpath('media')}))
