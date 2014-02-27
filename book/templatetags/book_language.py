'''
Created on Feb 27, 2014

@author: antipro
'''
from django import template
from django.template.base import TemplateSyntaxError
from book.models.language_book_preference import LanguagePreference
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.tag
def get_preference_language_id(parser, token):
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_current_language' requires 'as variable' (got %r)" % args)
    return BookPreferenceLanguageNode(args[2])

class BookPreferenceLanguageNode(template.Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        book = context["book"]
        user = context["user"]

        context[self.variable] = 0
        if user.is_authenticated():
            try:
                preference = LanguagePreference.objects.get(book=book, user=user)
                context[self.variable] = preference.language_id
            except ObjectDoesNotExist:
                pass

        return ""
