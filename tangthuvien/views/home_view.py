'''
Created on Jul 28, 2013

@author: antipro
'''
from django.template.response import TemplateResponse

from book.models import Book
from zinnia.models import Entry
from tangthuvien import settings
import datetime

def main(request, template="homepage.phtml"):
    data = {}

    data['show_top_banner'] = True

    last_update_time = datetime.datetime.now() - datetime.timedelta(**settings.HOMEPAGE_REGENT_BOOK_UPDATE_TIME)
    data['books'] = Book.objects.filter(last_update__gte=last_update_time).order_by('-last_update')

    data['entries'] = Entry.objects.all().order_by('-last_update')[0: settings.HOMEPAGE_RECENT_ENTRY_COUNT]  # @UndefinedVariable

    return TemplateResponse(request, template, data)
