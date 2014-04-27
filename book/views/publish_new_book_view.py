'''
Created on Oct 18, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.utils.decorators import method_decorator

from book.forms import PublishNewBookForm, AddAuthorForm, AddLanguageForm
from limiter.utils import LimitChecker

class PublishNewBookView(View):
    template="book/publish_new_book.html"
    post_new_book_form=PublishNewBookForm

    def _render(self, request, form):
        data = {}
        data['form'] = form
        author_form = AddAuthorForm(prefix='author')
        language_form = AddLanguageForm(prefix='language')

        data['author_form'] = author_form
        data['language_form'] = language_form

        return TemplateResponse(request, self.template, data)

    @method_decorator(login_required)
    def get(self, request):
        form = self.post_new_book_form(request.user)
        return self._render(request, form)

    @method_decorator(login_required)
    @LimitChecker.check("HOURLY_USER_PUBLISH_NEW_BOOK")
    @LimitChecker.check("HOURLY_IP_PUBLISH_NEW_BOOK")
    @LimitChecker.check("DAILY_USER_PUBLISH_NEW_BOOK")
    @LimitChecker.check("DAILY_IP_PUBLISH_NEW_BOOK")
    def post(self, request):
        form = self.post_new_book_form(request.user,
                                       data=request.POST,
                                       files=request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, _("New book was published successfully."))
            return HttpResponseRedirect(reverse('post_new_chapter',
                                                kwargs={'book_id':book.id}))

        return self._render(request, form)

LimitChecker.register(__name__, "HOURLY_USER_PUBLISH_NEW_BOOK",
                      _("You published %(counter)d of %(limit)d books in 1 hour. "
                        "So you can not publish any books until next hour. "
                        "Please try again"), 10, timeout_func='timeout_to_next_hour')

LimitChecker.register(__name__, "HOURLY_IP_PUBLISH_NEW_BOOK",
                      _("Your IP published %(counter)d of %(limit)d books in 1 hour. "
                        "So you can not publish any books until next hour. "
                        "Please try again"), 50, timeout_func='timeout_to_next_hour',
                      key_func='get_user_ip')

LimitChecker.register(__name__, "DAILY_USER_PUBLISH_NEW_BOOK",
                      _("You published %(counter)d of %(limit)d books today. "
                        "So you can not publish any books until next day. "
                        "Please try again"), 100, timeout_func='timeout_to_next_day')

LimitChecker.register(__name__, "DAILY_IP_PUBLISH_NEW_BOOK",
                      _("Your IP published %(counter)d of %(limit)d books today. "
                        "So you can not publish any books until next day. "
                        "Please try again"), 500, timeout_func='timeout_to_next_day',
                      key_func='get_user_ip')
