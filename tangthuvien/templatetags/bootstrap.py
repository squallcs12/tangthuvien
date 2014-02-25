'''
Created on Sep 21, 2013

@author: antipro
'''
from django import template
from ckeditor.widgets import CKEditorWidget

register = template.Library()

@register.filter(name='add_bootstrap_field')
def add_bootstrap_field(bound_field):
    bound_field.field.widget.attrs['class'] = 'form-control'
    if bound_field.field.required and not isinstance(bound_field.field.widget, CKEditorWidget):
        bound_field.field.widget.attrs['required'] = 'required'
    return bound_field

@register.inclusion_tag("_notification_message.phtml")
def render_message(message):
    message.tags_array = message.tags.split(" ")
    return {"message": message}