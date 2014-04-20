'''
Created on Apr 10, 2014

@author: eastagile
'''
from lettuce_setup.function import *
from book.models.copy_model import Copy
from book.features.factories.chapter_factory import ChapterFactory
from book.features.factories.book_factory import BookFactory
from book.models.book_model import Book
from book.features.steps.general import language

@step(u'thread with id "([^"]*)" was cloned to current site book id "([^"]*)"')
def thread_with_id_was_cloned_to_current_site_book_id(step, thread_id, book_id):
    book = BookFactory()
    book.id = int(book_id)
    book.save()
    book.languages.add(language())
    book.save()

    chapter = ChapterFactory()
    chapter.book = book
    chapter.language = language()
    chapter.number = 1
    chapter.save()

    Copy.objects.create(thread_id=thread_id,
                        book=book,
                        last_page=0,
                        last_post=0,
                        last_chapter_number=0,
                        is_done=0)

@step(u'I read thread "([^"]*)" on main site')
def i_read_thread_on_main_site(step, thread_id):
    visit_by_view_name("test_cloned_book_notification", kwargs={"thread_id": thread_id})

@step(u'I should be reading book id "([^"]*)"')
def i_should_be_reading_book_id(step, book_id):
    book = Book.objects.get(pk=int(book_id))
    browser().current_url.should.contain(book.get_absolute_url())

@step(u'I should not see any modal')
def i_should_not_see_any_dialog(step):
    find_all(".modal").should_not.be.ok
