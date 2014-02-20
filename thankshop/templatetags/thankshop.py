'''
Created on Sep 21, 2013

@author: antipro
'''
from django import template

register = template.Library()

@register.filter(name='thankshop_items')
def thankshop_items(user):
    return user.thankshop_items.all()
