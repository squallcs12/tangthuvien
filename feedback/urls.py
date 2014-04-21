'''
Created on Jul 28, 2013

@author: antipro
'''
from django.conf.urls import patterns, url
from feedback.views import FeedbackFormView

urlpatterns = patterns('',
    url(r'^form$', FeedbackFormView.as_view(), name='feedback_form'),
)
