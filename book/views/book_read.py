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
from django.contrib import messages
from django.utils.translation import ugettext as _
from book.models.language_book_preference import LanguagePreference
from tangthuvien.functions import UserSettings
from django.conf import settings

def main(request, slug, template="book/introduction.phtml"):
    data = {}
    book = Book.objects.get(slug=slug)
    data['book'] = book
    if request.user.is_authenticated():
        try:
            book_read_log = UserLog.objects.get(user=request.user, book=book)
            data['book_read_log'] = book_read_log
        except ObjectDoesNotExist:
            pass

    return TemplateResponse(request, template, data)


def chapter(request, slug, chapter_number, template="book/read.phtml"):
    data = {}
    book = Book.objects.get(slug=slug)
    data['book'] = book

    # check chapter available
    if book.chapter_set.filter(number=chapter_number).count() == 0:
        messages.warning(request, _("Chapter was not posed yet for this book."))
        return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number': 1}))

    # if user logged in
    if request.user.is_authenticated():
        chapter = None
        language_id = LanguagePreference.get_preference(user=request.user, book=book)  # get prefer language
        if language_id is not None:
            try:
                chapter = book.chapter_set.filter(number=chapter_number, language_id=language_id)[0]
            except IndexError:
                pass

        if chapter is None:
            language_preference_global = UserSettings.get(settings.BOOK_LANGUAGE_PREFER_KEY, request.user.id)
            if language_preference_global:
                for language_id in language_preference_global:
                    try:
                        chapter = book.chapter_set.filter(number=chapter_number, language_id=language_id)[0]
                        break
                    except:
                        pass

        if chapter is None:
            chapter = book.chapter_set.filter(number=chapter_number)[0]
    else:
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
