from django.views.generic.base import View
from django.template.response import TemplateResponse
from feedback.forms import FeedbackForm
from django.http.response import HttpResponse
import json
from django.utils.translation import ugettext

class FeedbackFormView(View):
    template_name = "feedback/form.html"

    def get(self, request):
        data = {}
        data['form'] = FeedbackForm()

        return TemplateResponse(request, self.template_name, data)

    def post(self, request):
        data = {}
        form = FeedbackForm(request.POST, request.FILES)

        if form.is_valid():
            form.save();
            response = HttpResponse("1")
            message = ugettext("Your feedback is sent. "
                               "We will work on that as soon as possible.")
            response['messages'] = json.dumps({"success": [message]})
            return response

        data['form'] = form

        return TemplateResponse(request, self.template_name, data)
