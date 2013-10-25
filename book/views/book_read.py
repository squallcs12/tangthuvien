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

    page = request.GET.get('page')

    if page is None and request.user.is_authenticated():
        try:
            page = UserLog.objects.get(user=request.user, book=book).page
            return HttpResponseRedirect(reverse('book_read', kwargs={'slug':book.slug}) + '?page=' + str(page))
        except ObjectDoesNotExist:
            pass

    chapter_list = book.chapter_set.all().order_by('number')
    paginator = Paginator(chapter_list, 1)

    try:
        chapters = paginator.page(page)
    except PageNotAnInteger:
        chapters = paginator.page(1)
    except EmptyPage:
        chapters = paginator.page(paginator.num_pages)

    data['chapters'] = chapters

    chapter = chapters[0]
    data['chapter'] = chapter

    chapter_read_signal.send(main, user=request.user, chapter=chapter, page=chapters.number)

    disqus_append(data)

    request.google_analytic.pageview['page'] = reverse('book_read', kwargs={'slug': book.slug})
    request.google_analytic.pageview['title'] = book.title

    data['config_reading_section_form'] = ConfigReadingSectionForm(request.user)

    return TemplateResponse(request, template, data)

def short(request, book_id):
    book_id = int(book_id)
    book = Book.objects.get(pk=book_id)
    return HttpResponseRedirect(reverse('book_read', kwargs={'slug':book.slug}))
