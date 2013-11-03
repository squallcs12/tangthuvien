from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tangthuvien.views.home_view.main', name='homepage'),

    url(r'^ttv/', include('tangthuvien.sub_urls')),

    # url(r'^tangthuvien/', include('tangthuvien.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # books
    url(r'^books/', include('book.urls')),

    # ckeditor
    url(r'^ckeditor/', include('ckeditor.urls')),

    # zinnia
    url(r'^blog/', include('zinnia.urls.capabilities')),
    url(r'^blog/feeds', include('zinnia.urls.feeds')),
    url(r'^blog/', include('zinnia.urls.entries')),
    url(r'^blog/', include('zinnia.urls.archives')),
    url(r'^blog/', include('zinnia.urls.shortlink')),

    url(r'^accounts/', include('accounts.urls')),

)

from tangthuvien import settings
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*\.(css|js|jpg|png|gif|bmp|ico|avi|mp3|mp4|wav|pdf|prc|zip|rar|doc))$',
                             'django.views.static.serve',
                            {'document_root': settings.realpath('media')}))
    # put the favicon in ano the place so that warning will not be thrown durring the test
    urlpatterns += patterns('', (r'^(?P<path>favicon\.ico)$', 'django.views.static.serve', {'document_root': settings.realpath('media')}))
