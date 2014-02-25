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
    parts = token.split_contents()
    tag_name, source_from, source_file = parts
    css_files.append((source_from, source_file))
    return EmptyCssNode(source_from, source_file)

@register.inclusion_tag
def load_js(parser, token):
    parts = token.split_contents()
    if parts[1] == "cdn":
        tag_name, source_from, source_file, cdn_url = parts
        if settings.DEBUG:
            source_from = "static"
        else:
            source_from = "url"
            source_file = cdn_url
    else:
        tag_name, source_from, source_file = parts

    return EmptyJsNode(source_from, source_file)

@register.tag
def print_css(parser, token):
    import pdb;pdb.set_trace()
    return PrintCssNode()

@register.tag
def print_js(parser, token):
    return PrintJsNode()

class EmptyNode(template.Node):
    var_name = "css_files"
    def __init__(self, source_from, source_file, *args, **kwargs):
        self.source_from = source_from
        self.source_file = source_file
        super(template.Node, self).__init__(*args, **kwargs)

    def render(self, context):
        if not hasattr(context["request"], self.var_name):
            setattr(context["request"], self.var_name, [])
        getattr(context["request"], self.var_name).append((self.source_from, self.source_file))
        print getattr(context["request"], self.var_name)
        return ''

class EmptyJsNode(EmptyNode):
    var_name = "js_files"

class EmptyCssNode(EmptyNode):
    var_name = "css_files"


class PrintCssNode(template.Node):
    source_froms = {
        'static' : settings.STATIC_URL + "css",
        'media'  : settings.MEDIA_URL + "css",
        'url'    : '',
    }
    def render(self, context):
        output = ''
        for source_from, source_file in reversed(context["request"].css_files):
            source_file = template.Template(source_file).render(context)
            source_from = template.Template(source_from).render(context)
            output += '<link rel="stylesheet" type="text/css" href="%s%s" />' % (self.source_froms[source_from], source_file,)
        return output

class PrintJsNode(template.Node):
    source_froms = {
        'static' : settings.STATIC_URL + "js",
        'media'  : settings.MEDIA_URL + "js",
        'url'    : '',
    }
    def render(self, context):
        output = ''
        for source_from, source_file in reversed(context["request"].js_files):
            source_file = template.Template(source_file).render(context)
            source_from = template.Template(source_from).render(context)
            output += '<script src="%s%s"></script>' % (self.source_froms[source_from], source_file,)
        return output
