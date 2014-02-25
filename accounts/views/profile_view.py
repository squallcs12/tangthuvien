'''
Created on Sep 18, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib import messages
def main(request, template="accounts/profile.phtml"):
    data = {}
    messages.success(request, "thankshop/daily_thankpoints_increase.phtml", extra_tags="template")
    return TemplateResponse(request, template, data)
