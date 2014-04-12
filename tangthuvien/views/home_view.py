'''
Created on Jul 28, 2013

@author: antipro
'''
from django.template.response import TemplateResponse

from book.models import Book
from tangthuvien import settings
import datetime

def main(request, template="homepage.phtml"):
    data = {}

    data['show_top_banner'] = True
    for time_settings in settings.HOMEPAGE_RECENT_BOOK_UPDATE_TIME:
    	last_update_time = datetime.datetime.now() - datetime.timedelta(**time_settings)
    	data['books'] = Book.objects.filter(last_update__gte=last_update_time,
    									chapters_count__gt=0).order_by('-last_update')
    	if data['books'].count():
    		break

    return TemplateResponse(request, template, data)
