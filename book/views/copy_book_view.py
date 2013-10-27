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
import subprocess
from tangthuvien import settings

def get_log_file(book_id):
    return settings.realpath('log/copybook/%s.log' % book_id)

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

    thread_url = request.GET.get('url')
    thread_id = thread_url.split('?')[1].split('=')[1]

    subprocess.Popen([
        settings.realpath('env/bin/python'),
        'manage.py',
        'copybook',
        '-b %s' % book.id,
        '-t %s' % thread_id,
        '-l %s' % get_log_file(book.id),
    ])

    return TemplateResponse(request, template, data)

@login_required
def process_output(request, book_id=0):
    response = HttpResponse()
    start_line = int(request.GET.get('start_line', 0))
    log_file = get_log_file(book.id)
    with open(log_file, 'r') as fb:
        for i, line in enumerate(fp):
            if i >= start_line:
                response.write("%s\n" % line)
    return response