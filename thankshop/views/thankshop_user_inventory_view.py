'''
Created on Dec 15, 2013

@author: antipro
'''
from django.template.response import TemplateResponse

def index(request, username="me", template="thankshop/inventory.phtml"):
    data = {}

    return TemplateResponse(request, template, data)
