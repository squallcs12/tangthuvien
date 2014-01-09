'''
Created on Jul 29, 2013

@author: antipro
'''
from django import template

from tangthuvien import settings

register = template.Library()

css_files = []
js_files = []

@register.tag
def load_css(parser, token):
    tag_name, source_from, source_file = token.split_contents()
    css_files.append((source_from, source_file))
    return EmptyNode()

@register.tag
def load_js(parser, token):
    tag_name, source_from, source_file = token.split_contents()
    js_files.append((source_from, source_file))
    return EmptyNode()

@register.tag
def print_css(parser, token):
    return PrintCssNode()

@register.tag
def print_js(parser, token):
    return PrintJsNode()

class EmptyNode(template.Node):
    def render(self, context):
        return ''

class PrintCssNode(template.Node):
    source_froms = {
        'static' : settings.STATIC_URL + "css",
        'media'  : settings.MEDIA_URL + "css",
        'url'    : '',
    }
    def render(self, context):
        if settings.DEBUG:
            output = ''
            for source_from, source_file in reversed(css_files):
                output += '<link rel="stylesheet" type="text/css" href="%s%s" />' % (self.source_froms[source_from], source_file,)
            return output
        else:
            raise NotImplemented()

class PrintJsNode(template.Node):
    source_froms = {
        'static' : settings.STATIC_URL + "js",
        'media'  : settings.MEDIA_URL + "js",
        'url'    : '',
    }
    def render(self, context):
        if settings.DEBUG:
            output = ''
            for source_from, source_file in reversed(js_files):
                output += '<script src="%s%s"></script>' % (self.source_froms[source_from], source_file,)
            return output
        else:
            raise NotImplemented()
