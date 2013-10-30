'''
Created on Aug 16, 2013

@author: antipro
'''
from tangthuvien.decorator.ajax_required_decorator import ajax_required
from book.models.book_model import Book
from book.models.favorite_model import Favorite
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from tangthuvien.django_custom import HttpGoBack, HttpJson

@ajax_required
@login_required
def ajax_submit(request):
    returnJson = {}
    book_id = int(request.POST.get('id'))

    book = Book.objects.get(pk=book_id)
    try:
        Favorite.objects.get(user=request.user, book=book).delete()
    except ObjectDoesNotExist:
        favorite = Favorite(user=request.user, book=book)
        book.favorite_set.add(favorite)

    return HttpJson(returnJson)

@login_required
def unfavorite_books(request):
    for book_id in request.POST.getlist('ids[]'):
        book = Book.objects.get(pk=int(book_id))
        Favorite.objects.get(user=request.user, book=book).delete()

    return HttpGoBack(request)

@login_required
def main(request, template="book/favorite.phtml"):
    data = {}
    books = request.user.favorite_books.all()
    data['books'] = books

    return TemplateResponse(request, template, data)
