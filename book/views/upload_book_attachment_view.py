from tangthuvien.django_custom import HttpJson
from book.models import Book

def ajax(request, book_id):
	returnJson = {}

	book = Book.objects.get(pk=book_id)

	returnJson['status'] = 'success'
	returnJson['files'] = ['fiel.jpg']
	return HttpJson(returnJson)