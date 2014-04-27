'''
Created on Apr 25, 2014

@author: antipro
'''
from django import template
from limiter.utils import LimitChecker

register = template.Library()

@register.tag
def get_limter_counter(parser, token):
    _, code = token.contents.split()
    return GetLimiterCounterNode(code)

@register.tag
def get_limter_key(parser, token):
    _, code = token.contents.split()
    return GetLimiterKeyNode(code)

class GetLimiterCounterNode(template.Node):
    def __init__(self, code):
        self.code = template.Variable(code)

    def render(self, context):
        code = self.code.resolve(context)
        return LimitChecker.get_counter(code, context['request'])

class GetLimiterKeyNode(template.Node):
    def __init__(self, code):
        self.code = template.Variable(code)

    def render(self, context):
        code = self.code.resolve(context)
        return LimitChecker.get_key(code, context['request'])
