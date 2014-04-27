'''
Created on Sep 21, 2013

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

from book.models.book_model import Book
from book.forms import PostNewChapterForm
from limiter.utils import LimitChecker


class PostNewChapterView(View):

    template = "book/post_new_chapter.html"
    post_new_chapter_form=PostNewChapterForm

    def _render(self, request, book, form):
        data = {}
        data['book'] = book
        data['form'] = form
        return TemplateResponse(request, self.template, data)

    @method_decorator(login_required)
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        form = self.post_new_chapter_form(book, request.user)
        return self._render(request, book, form)

    @method_decorator(login_required)
    @LimitChecker.check("HOURLY_USER_PUBLISH_NEW_CHAPTER")
    @LimitChecker.check("HOURLY_IP_PUBLISH_NEW_CHAPTER")
    @LimitChecker.check("DAILY_USER_PUBLISH_NEW_CHAPTER")
    @LimitChecker.check("DAILY_IP_PUBLISH_NEW_CHAPTER")
    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        form = self.post_new_chapter_form(book, request.user, request.POST)
        if form.is_valid():
            chapter = form.save()
            messages.success(request, _('New chapter was posted successfully.'))
            return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number': chapter.number}))
        return self._render(request, book, form)

LimitChecker.register(__name__, "HOURLY_USER_PUBLISH_NEW_CHAPTER",
                      _("You published %(counter)d of %(limit)d chapters in 1 hour. "
                        "So you can not publish any chapters until next hour. "
                        "Please try again"), 100, timeout_func='timeout_to_next_hour')

LimitChecker.register(__name__, "HOURLY_IP_PUBLISH_NEW_CHAPTER",
                      _("Your IP published %(counter)d of %(limit)d chapters in 1 hour. "
                        "So you can not publish any chapters until next hour. "
                        "Please try again"), 500, timeout_func='timeout_to_next_hour',
                      key_func='get_user_ip')

LimitChecker.register(__name__, "DAILY_USER_PUBLISH_NEW_CHAPTER",
                      _("You published %(counter)d of %(limit)d chapters today. "
                        "So you can not publish any chapters until next day. "
                        "Please try again"), 300, timeout_func='timeout_to_next_day')

LimitChecker.register(__name__, "DAILY_IP_PUBLISH_NEW_CHAPTER",
                      _("Your IP published %(counter)d of %(limit)d chapters today. "
                        "So you can not publish any chapters until next day. "
                        "Please try again"), 1000, timeout_func='timeout_to_next_day',
                      key_func='get_user_ip')
