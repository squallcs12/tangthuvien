'''
Created on Aug 23, 2013

@author: antipro
'''
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME

def HttpJson(obj):
    return HttpResponse(simplejson.dumps(obj, cls=DjangoJSONEncoder), content_type="application/json")

def get_go_back_url(request, redirect_fieldname=REDIRECT_FIELD_NAME, default='/'):
    redirect_to = request.REQUEST.get(redirect_fieldname)
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = resolve_url(default) if default else None
    return redirect_to

def HttpGoBack(request, redirect_fieldname=REDIRECT_FIELD_NAME, default='/'):
    redirect_to = get_go_back_url(request, redirect_fieldname)
    return HttpResponseRedirect(redirect_to)
