'''
Created on Dec 14, 2013

@author: antipro
'''
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from thankshop import models

def index(request, template="thankshop/shop_homepage.phtml"):
    data = {}

    items = models.Item.objects.all().filter(stocks__gt=0)
    data['items'] = items

    return TemplateResponse(request, template, data)
