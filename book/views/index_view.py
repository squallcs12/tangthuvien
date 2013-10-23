'''
Created on Jul 28, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from book.models import Book
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from tangthuvien import settings
from book.signals import pre_listing_book
from book.models.category_model import Category
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from tangthuvien.django_custom import HttpJson
from django.http.response import HttpResponseRedirect

def main(request, template='book/index.phtml'):
    data = {}

    page = request.GET.get('page')
    perpage = request.GET.get('perpage', settings.BOOK_LIST_ITEM_COUNT)

    book_list = Book.objects.filter(chapters_count__gt=0)
    paginator = Paginator(book_list, perpage)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    data['books'] = books

    data['categories'] = Category.objects.values('id', 'title')

    pre_listing_book.send(main, user=request.user, books=books)

    return TemplateResponse(request, template, data)

def ajax(request, template='book/_books_list_index.phtml'):
    data = {}
    returnJson = {}

    page = request.GET.get('page')
    perpage = request.GET.get('perpage', settings.BOOK_LIST_ITEM_COUNT)

    book_list = Book.objects.filter(chapters_count__gt=0)

    categories = request.GET.get('categories')
    if categories:
        categories = [int(category_id) for category_id in categories.split(',')]
        for category_id in categories:
            book_list = book_list.filter(categories__pk=category_id)

    paginator = Paginator(book_list, perpage)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    data['books'] = books
    data['showcheckbox'] = False

    returnJson['content'] = render_to_string(template, data)

    sorted(categories)
    category_slugs = ",".join(Category.objects.get(pk=category_id).slug for category_id in categories)
    returnJson['url'] = reverse('books_list_by_categories', kwargs={'slugs': category_slugs})

    title = " ".join(Category.objects.get(pk=category_id).title for category_id in categories)
    returnJson['title'] = title

    return HttpJson(returnJson)


def by_categories(request, template='book/index.phtml', slugs=''):
    data = {}

    page = request.GET.get('page')
    perpage = request.GET.get('perpage', settings.BOOK_LIST_ITEM_COUNT)

    if not slugs:
        return HttpResponseRedirect(reverse('books_home'))

    categories = Category.objects.filter(slug__in=slugs.split(','))

    book_list = Book.objects.filter(chapters_count__gt=0)
    for category in categories:
        book_list = book_list.filter(categories__pk=category.id)

    paginator = Paginator(book_list, perpage)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    data['books'] = books

    data['categories'] = Category.objects.values('id', 'title')

    data['selectedCategories'] = categories

    pre_listing_book.send(main, user=request.user, books=books)

    return TemplateResponse(request, template, data)


