from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tangthuvien.functions import UserSettings
from tangthuvien import settings
from book import models
import json

class LanguageSettingView(View):
    template = "book/language_setting.phtml"

    def get(self, request):
        data = {}

        data['active_languagesetting'] = True # active menu language settings
        data['language_prefer'] = UserSettings.get(settings.BOOK_LANGUAGE_PREFER_KEY, request.user.id)
        return TemplateResponse(request, self.template, data)

    @method_decorator(login_required)
    def post(self, request):
        settings_dict = json.loads(request.body)

        # make sure settings is valid
        for value in settings_dict:
            int(value) # if fail then 500 error will be thrown

        UserSettings.set(settings.BOOK_LANGUAGE_PREFER_KEY, request.user.id, settings_dict)
        return HttpResponse("1")