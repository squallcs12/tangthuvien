'''
Created on Jul 28, 2013

@author: antipro
'''
from django.conf.urls import patterns, include, url


urlpatterns = patterns('book.views',
    url(r'^$', 'index_view.main', name='books_home'),
)