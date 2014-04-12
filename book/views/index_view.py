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
from tangthuvien.django_custom import HttpJson
from book.models.author_model import Author
from django.core.exceptions import ObjectDoesNotExist


def by_categories(func):
    def decorator(request):
        book_list, context = func(request)

        slugs = request.REQUEST.get('categories')
        ids = request.REQUEST.get('category_ids')

        if slugs or ids:
            if slugs:
                categories = Category.objects.filter(slug__in=slugs.split(','))
            elif ids:
                categories = Category.objects.filter(id__in=[int(_id) for _id in ids.split(',')])
            if categories:
                for category in categories:
                    book_list = book_list.filter(categories__pk=category.id)

                context['selectedCategories'] = categories
                context['page_title'] = " ".join(category.title for category in categories)

                if len(categories) == 1:
                    context['page_description'] = categories[0].description
                else:
                    context['page_description'] = context['page_title']

                if request.is_ajax():
                    context['category_slugs'] = ",".join(category.slug for category in categories)

        return book_list, context

    return decorator

def by_author(func):
    def decorator(request):
        book_list, context = func(request)

        author_slug = request.REQUEST.get('author')
        if author_slug:
            try:
                author = Author.objects.get(slug=author_slug)
                book_list = book_list.filter(author=author)
                context['author'] = author
            except ObjectDoesNotExist:
                pass
        return book_list, context

    return decorator

@by_categories
@by_author
def get_book_list(request):
    book_list = Book.objects.filter(chapters_count__gt=0)
    return book_list, {}

def main(request, template='book/index.phtml'):
    data = {}

    page = request.REQUEST.get('page')
    perpage = request.REQUEST.get('perpage', settings.BOOK_LIST_ITEM_COUNT)

    book_list, context = get_book_list(request)
    data.update(**context)

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

    book_list, context = get_book_list(request)
    data.update(**context)

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
    if 'category_slugs' in context:
        returnJson['category_slugs'] = context['category_slugs']

    return HttpJson(returnJson)

