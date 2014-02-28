'''
Created on Feb 23, 2014

@author: antipro
'''
from thankshop import models
from tangthuvien.django_custom import HttpJson

def list_items(request):
    items = models.Item.objects.all().filter(stocks__gt=0)

    return HttpJson(items)

def get_item(request, item_id):
    pass
