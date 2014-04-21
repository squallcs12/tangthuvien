'''
Created on Apr 10, 2014

@author: eastagile
'''
from django.template.response import TemplateResponse
from django.views.generic.base import View
from book.models.copy_model import Copy
from django.core.exceptions import ObjectDoesNotExist

class TestClonedBookNotificationView(View):
    template_name = "book/test_cloned_notification.html"

    def get(self, request, thread_id):
        data = {}
        data['thread_id'] = thread_id

        return TemplateResponse(request, self.template_name, data)

class ClonedBookJsNotificationView(View):
    template_name = "book/cloned_js_notification.html"

    def get(self, request, thread_id):
        data = {}
        data['thread_id'] = thread_id

        try:
            copy = Copy.objects.get(thread_id=thread_id)
            data['book'] = copy.book
        except ObjectDoesNotExist:
            pass

        response = TemplateResponse(request, self.template_name, data)

        response['Content-type'] = 'application/javascript'

        return response
