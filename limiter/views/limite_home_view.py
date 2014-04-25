'''
Created on Apr 25, 2014

@author: antipro
'''
from django.views.generic.list import ListView
from limiter.models import Tracker


class LimiterHomeView(ListView):
    model = Tracker
