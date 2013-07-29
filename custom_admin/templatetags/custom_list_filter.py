'''
Created on Jul 29, 2013

@author: antipro
'''
from django import template
from custom_admin.filters import TextColumnFilter

register = template.Library()

@register.tag
def admin_column_filter(parser, token):
    tag_name, header = token.split_contents()
    return ColumnFilterNode(header)

class ColumnFilterNode(template.Node):
    def __init__(self, header):
        self.header_param = header

    def render(self, context):
        column_name = context[self.header_param]['text'].lower().replace(' ', '_')
        column_filters = context['cl'].model_admin.current_column_filters

        if column_name in column_filters:
            return column_filters[column_name].render()
        elif column_name in context['cl'].model_admin.list_display:
            return TextColumnFilter(column_name).render()

        return ''
