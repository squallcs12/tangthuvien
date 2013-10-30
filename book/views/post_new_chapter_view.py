'''
Created on Sep 21, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from book.models.book_model import Book
from django.contrib.auth.decorators import login_required
from book.forms import PostNewChapterForm
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

@login_required
def main(request, book_id, post_new_chapter_form=PostNewChapterForm, template="book/post_new_chapter.phtml"):
    data = {}
    book = Book.objects.get(pk=book_id)
    data['book'] = book

    if request.method == "POST":
        form = post_new_chapter_form(request, book, data=request.POST)
        if form.is_valid():
            chapter = form.process()
            return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number': chapter.number}))
    else:
        form = post_new_chapter_form(request, book)

    data['form'] = form

    return TemplateResponse(request, template, data)
