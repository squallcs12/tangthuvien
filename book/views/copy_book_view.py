'''
Created on Oct 23, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from book.forms import CopyBookForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from book.models.book_model import Book
from django.http import StreamingHttpResponse
import time
import pdb
from book.management.commands import copybook

@login_required
def main(request, post_new_book_form=CopyBookForm, template="book/copy_book.phtml"):
    data = {}

    if request.method == "POST":
        form = post_new_book_form(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.process()
            return HttpResponseRedirect("%s?url=%s" % (reverse('copy_book_process', kwargs={'book_id':book.id}), form.cleaned_data['thread_url']))
    else:
        form = post_new_book_form(request)

    data['form'] = form

    return TemplateResponse(request, template, data)

@login_required
def process(request, book_id=0, template="book/copy_book_process.phtml"):
    data = {}

    book = Book.objects.get(pk=book_id)
    data['book'] = book

    data['url'] = request.GET.get('url')

    return TemplateResponse(request, template, data)

@login_required
def process_output(request, book_id=0):

    thread_url = request.GET.get('url')
    thread_id = thread_url.split('?')[1].split('=')[1]

    def copy_output():
        for message in copybook.Command().copy(thread_id, book_id, 1, 0):
            yield "window.parent.report_copy_process('%s');" % message
    resp = StreamingHttpResponse(copy_output())
    return resp

