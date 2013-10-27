'''
Created on Oct 27, 2013

@author: antipro
'''
from django import template
register = template.Library()

@register.filter(name='size_in_kb')
def to_list(size_in_byte):
    return "%s KB" % (size_in_byte / 1024)
