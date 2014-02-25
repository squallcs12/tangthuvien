'''
Created on Feb 23, 2014

@author: antipro
'''
'''
Created on Jul 29, 2013

@author: antipro
'''
from django import template

from tangthuvien import settings

register = template.Library()

ANGULAR_REQUIRES = []

@register.tag
def angular_require(parser, token):
    requires = token.split_contents()[1:]
    for require in requires:
        ANGULAR_REQUIRES.append(require)
    return EmptyNode()

class EmptyNode(template.Node):
    def render(self, context):
        return ''

@register.tag
def print_angular_require(parser, token):
    return PrintAngularRequireNode()

class PrintAngularRequireNode(template.Node):
    return ANGULAR_REQUIRES
