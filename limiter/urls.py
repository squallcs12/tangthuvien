'''
Created on Apr 25, 2014

@author: antipro
'''
from django.conf.urls import patterns, url
from limiter.views.limite_home_view import LimiterHomeView
urlpatterns = patterns('',
    url(r'^$', LimiterHomeView.as_view(), name='limiter_home'),
)
