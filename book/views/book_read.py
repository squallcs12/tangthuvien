'''
Created on Jul 29, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from book.models.book_model import Book
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from book.signals import chapter_read_signal
from book.models.user_log_model import UserLog
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tangthuvien.functions import disqus_append
from book.forms import ConfigReadingSectionForm

def main(request, slug, template="book/read.phtml"):
    data = {}
    book = Book.objects.get(slug=slug)
    data['book'] = book
    
    if request.user.is_authenticated():
        try:
            page = UserLog.objects.get(user=request.user, book=book).page
            return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number' : page}))
        except ObjectDoesNotExist:
            pass
    
    return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number' : 1}))
    

def chapter(request, slug, chapter_number, template="book/read.phtml"):
    data = {}
    book = Book.objects.get(slug=slug)
    data['book'] = book

    chapter = book.chapter_set.filter(number=chapter_number)[0]
    data['chapter'] = chapter

    chapter_read_signal.send(main, user=request.user, chapter=chapter)

    disqus_append(data)

    request.google_analytic.pageview['page'] = reverse('book_read', kwargs={'slug': book.slug})
    request.google_analytic.pageview['title'] = book.title

    data['config_reading_section_form'] = ConfigReadingSectionForm(request.user)

    return TemplateResponse(request, template, data)

def short(request, book_id):
    book_id = int(book_id)
    book = Book.objects.get(pk=book_id)
    return HttpResponseRedirect(reverse('book_read', kwargs={'slug':book.slug}))
