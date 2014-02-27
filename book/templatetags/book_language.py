'''
Created on Feb 27, 2014

@author: antipro
'''
from django import template
from django.template.base import TemplateSyntaxError
from book.models.language_book_preference import LanguagePreference
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='chapters_paging')
def chapters_paging(chapters_list, chapter):
    language_chapter_list = chapters_list[chapter.language_id]
    for index, chapter_info in enumerate(language_chapter_list):
        if chapter_info[0] == chapter.number:
            if index > 0:
                yield language_chapter_list[index - 1][0]
            yield chapter.number
            if index < len(language_chapter_list) - 1:
                yield language_chapter_list[index + 1][0]

@register.filter(name='filter_by_language')
def filter_by_language(chapters_list, language_id):
    return chapters_list[language_id]

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
                context[self.variable] = LanguagePreference.get_preference(book, user)
            except ObjectDoesNotExist:
                pass
        if not context[self.variable]:
            context[self.variable] = book.languages.all()[0].id

        return ""
