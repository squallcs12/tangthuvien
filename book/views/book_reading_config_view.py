'''
Created on Oct 26, 2013

@author: antipro
'''
from book.forms import ConfigReadingSectionForm
from django.http.response import HttpResponse
from decorator.ajax_required_decorator import ajax_required
from django.contrib.auth.decorators import login_required

@ajax_required
@login_required
def ajax(request):
    form = ConfigReadingSectionForm(request.user, request.POST)
    if form.is_valid():
        form.process()
        return HttpResponse('1')
    return HttpResponse('0')
