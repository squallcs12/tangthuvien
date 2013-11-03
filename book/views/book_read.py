'''
Created on Jul 29, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from book.models.book_model import Book
from book.signals import chapter_read_signal
from book.models.user_log_model import UserLog
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from book.forms import ConfigReadingSectionForm

def main(request, slug, template="book/introduction.phtml"):
    data = {}
    book = Book.objects.get(slug=slug)
    data['book'] = book

    if request.user.is_authenticated():
        try:
            book_read_log = UserLog.objects.get(user=request.user, book=book)
            data['book_read_log'] = book_read_log
            if not request.GET.get('r'):
                page = book_read_log.page
                return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number' : page}))
        except ObjectDoesNotExist:
            pass

    return TemplateResponse(request, template, data)


def chapter(request, slug, chapter_number, template="book/read.phtml"):
    data = {}
    book = Book.objects.get(slug=slug)
    data['book'] = book

    chapter = book.chapter_set.filter(number=chapter_number)[0]
    data['chapter'] = chapter

    chapter_read_signal.send(main, user=request.user, chapter=chapter)

    request.google_analytic.pageview['page'] = reverse('book_read', kwargs={'slug': book.slug})
    request.google_analytic.pageview['title'] = book.title

    data['config_reading_section_form'] = ConfigReadingSectionForm(request.user)

    return TemplateResponse(request, template, data)

def short(request, book_id):
    book_id = int(book_id)
    book = Book.objects.get(pk=book_id)
    return HttpResponseRedirect(reverse('book_read', kwargs={'slug':book.slug}))
