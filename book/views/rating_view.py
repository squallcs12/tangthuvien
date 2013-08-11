'''
Created on Aug 8, 2013

@author: antipro
'''
from django.http.response import HttpResponse
from tangthuvien.decorator.ajax_required_decorator import ajax_required
from book.models.book_model import Book
import json

@ajax_required
def main(request):
    number = int(request.POST.get('number'))
    book_id = int(request.POST.get('book_id'))

    book = Book.objects.get(pk=book_id)
    if number not in range(1, 6):
        raise NotImplemented()

    book.rating.add_rating(request.user, number)

    returnJson = {}
    returnJson['average_result'] = book.rating.average_result
    returnJson['rating_count'] = book.rating.rating_count

    return HttpResponse(json.dumps(returnJson), content_type="application/json")
