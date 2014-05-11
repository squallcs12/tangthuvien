'''
Created on May 11, 2014

@author: antipro
'''

from django.conf.urls import patterns, url
from web_image.views import WebImageGenerateView
urlpatterns = patterns('book.views',
    url(r'^generate$', WebImageGenerateView.as_view(), name='web_image_generate'),
)
