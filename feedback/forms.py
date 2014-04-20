'''
Created on Apr 19, 2014

@author: antipro
'''
from django.forms.models import ModelForm
from feedback.models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ('ip', 'date')
