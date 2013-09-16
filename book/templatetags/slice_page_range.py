'''
Created on Sep 16, 2013

@author: antipro
'''

from django import template
from tangthuvien import settings

register = template.Library()

@register.filter(name='slice_page_range')
def slice_page_range(pagination):
    page_range = pagination.paginator.page_range
    for number in settings.BOOK_CHAPTER_PAGINATOR_RANGE:
        page_number = pagination.number + number
        if page_number in page_range:
            yield page_number
