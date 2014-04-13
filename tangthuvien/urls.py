from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tangthuvien.views.home_view.main', name='homepage'),
    url(r'^testimonials', 'tangthuvien.views.testimonials_view.index', name='testimonials'),

    url(r'^ttv/', include('tangthuvien.sub_urls')),

    # url(r'^tangthuvien/', include('tangthuvien.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/lookups/', include('ajax_select.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # books
    url(r'^books/', include('book.urls')),

    # ckeditor
    url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^accounts/', include('accounts.urls')),

    # thankshop
    url(r'^thankshop/', include('thankshop.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
