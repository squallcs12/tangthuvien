'''
Created on Sep 18, 2013

@author: antipro
'''
from django.template.response import TemplateResponse

def main(request, template="accounts/profile.phtml"):
    data = {}
    data['active_profile'] = True
    return TemplateResponse(request, template, data)
