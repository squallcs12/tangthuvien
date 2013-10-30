'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien.django_custom import HttpGoBack
from django.contrib.auth.decorators import login_required
from tangthuvien.context_processors import ChangeStyle_processor

@login_required
def change(request, style):
    ChangeStyle_processor.set_style(request.user, style)
    return HttpGoBack(request)
