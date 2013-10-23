'''
Created on Sep 21, 2013

@author: antipro
'''
from django import template

register = template.Library()

@register.filter(name='add_bootstrap_field')
def add_bootstrap_field(bound_field):
    bound_field.field.widget.attrs['class'] = 'form-control'
    return bound_field
