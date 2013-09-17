'''
Created on Sep 17, 2013

@author: antipro
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('tangthuvien.views',
    url(r'^submit_onetime_notification', 'onetime_notification_view.submit', name='submit_onetime_notification'),
)
