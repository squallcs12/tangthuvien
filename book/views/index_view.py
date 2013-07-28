'''
Created on Jul 28, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from book.models import Book
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from tangthuvien import settings
def main(request, template='book/index.phtml'):
    data = {}

    page = request.GET.get('page')
    perpage = request.GET.get('perpage', settings.BOOK_LIST_ITEM_COUNT)

    book_list = Book.objects.all()
    paginator = Paginator(book_list, perpage)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    data['books'] = books

    return TemplateResponse(request, template, data)
