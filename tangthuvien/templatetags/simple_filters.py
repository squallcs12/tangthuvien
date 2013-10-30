'''
Created on Oct 22, 2013

@author: antipro
'''
from django import template
register = template.Library()

@register.filter(name='list')
def to_list(obj):
    return list(obj)

@register.filter(name='multiple')
def multiple(number, multipler):
    return number * multipler


