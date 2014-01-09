'''
Created on Jul 28, 2013

@author: antipro
'''
from django.template.response import TemplateResponse

def index(request, template="testimonials.phtml"):
    data = {}

    data['show_top_banner'] = True

    return TemplateResponse(request, template, data)
