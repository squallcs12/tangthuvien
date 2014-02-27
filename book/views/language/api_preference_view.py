from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tangthuvien.django_custom import HttpJson, HttpGoBack
from book.models import Language
from book.models.book_model import Book
from book.models.language_book_preference import LanguagePreference
from django.core.exceptions import ObjectDoesNotExist

class LanguagePreferenceView(View):

    @method_decorator(login_required)
    def get(self, request):
        language_id = int(request.GET.get('language_id'))
        book_id = int(request.GET.get('book_id'))
        self.change_language_preference(request.user, book_id, language_id)
        return HttpGoBack(request)

    @method_decorator(login_required)
    def post(self, request):
        language_id = int(request.POST.get('language_id'))
        book_id = int(request.POST.get('book_id'))
        self.change_language_preference(request.user, book_id, language_id)
        return HttpJson("1")

    def change_language_preference(self, user, book_id, language_id):
        book = Book.objects.get(pk=book_id)
        language = Language.objects.get(pk=language_id)

        try:
            preference = LanguagePreference.objects.get(user=user, book=book)
            preference.language = language
        except ObjectDoesNotExist:
            preference = LanguagePreference(user=user, book=book, language=language)
        preference.save()

