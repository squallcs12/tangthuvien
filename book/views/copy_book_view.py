'''
Created on Oct 23, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from book.forms import CopyBookForm, AddAuthorForm, AddLanguageForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from book.models.book_model import Book
from tangthuvien import settings
import os
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from limiter.utils import LimitChecker

def get_log_file(book_id):
    return settings.realpath('log/copybook/%s.log' % book_id)

class CopyNewBookView(View):
    template="book/copy_book.html"
    post_new_book_form=CopyBookForm

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
        form = self.post_new_book_form(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save()
            return HttpResponseRedirect("%s?url=%s&skip=%s" % (
                                                       reverse('copy_book_process', kwargs={'book_id':book.id}),
                                                       form.cleaned_data['thread_url'],
                                                       1 if form["skip_first_post"].value() else 0,
                                                       ))
        return self._render(request, form)

@login_required
def process(request, book_id=0, template="book/copy_book_process.html"):
    data = {}

    book = Book.objects.get(pk=book_id)
    data['book'] = book

    thread_url = request.GET.get('url')
    thread_id = thread_url.split('?')[1].split('=')[1]
    skip = request.GET.get("skip")

    os.system(" ".join([
        settings.realpath('env/bin/python'),
        settings.realpath('manage.py'),
        'copybook',
        '-b %s' % book.id,
        '-t %s' % thread_id,
        '-l %s' % get_log_file(book.id),
        '--skip=%s' % skip,
        "&"
    ]))

    return TemplateResponse(request, template, data)

@login_required
def sync(request, book_id=0, template="book/copy_book_process.html"):
    data = {}

    book = Book.objects.get(pk=book_id)
    data['book'] = book

    thread_id = book.copy.thread_id

    sync_command = " ".join([
        settings.realpath('env/bin/python'),
        settings.realpath('manage.py'),
        'copybook',
        '-b %s' % book.id,
        '-t %s' % thread_id,
        '-s %s' % book.copy.last_page,
        '-p %s' % book.copy.last_post,
        '-l %s' % get_log_file(book.id),
        "&"
    ])
    os.system(sync_command)

    return TemplateResponse(request, template, data)

@login_required
def process_output(request, book_id=0):
    response = HttpResponse()
    start_line = int(request.GET.get('start_line', 0))
    log_file = get_log_file(book_id)
    with open(log_file, 'r') as fp:
        for i, line in enumerate(fp):
            if i >= start_line:
                response.write(line)
    return response
