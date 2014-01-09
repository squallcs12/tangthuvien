'''
Created on Nov 16, 2013

@author: antipro
'''
from tangthuvien import settings
from book.models.book_model import Book
from django.utils.translation import ugettext as _
from django.contrib import messages
from tangthuvien.django_custom import HttpGoBack

import os
from django.http.response import HttpResponse

def main(request, book_id):
    generate_prc(book_id)
    messages.success(request, _("Book generate PRC process was started. The PRC file will be listed once this process finished."))
    return HttpGoBack(request)

def ajax(request, book_id):
    generate_prc(book_id)
    return HttpResponse("1")

def generate_prc(book_id):
    book = Book.objects.get(pk=book_id)
    sync_command = " ".join([
        settings.realpath('env/bin/python'),
        settings.realpath('manage.py'),
        'generate_prc',
        '-b %s' % book.id,
        "&"
    ])
    os.system(sync_command)
