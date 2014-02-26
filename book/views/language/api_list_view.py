from django.views.generic.base import View
from tangthuvien.django_custom import HttpJson
from book.models import Language

class LanguageListView(View):

    def get(self, request):
        languages = Language.objects.all()

        return HttpJson(languages)
