'''
Created on Apr 10, 2014

@author: eastagile
'''
from lettuce_setup.function import *
from book.models.copy_model import Copy
from book.features.factories.author_factory import AuthorFactory
from book.models.author_model import Author
from book.features.factories.chapter_factory import ChapterFactory
from book.features.factories.book_factory import BookFactory
from book.models.language_model import Language
from book.features.factories.language_factory import LanguageFactory
from book.models.book_model import Book

def author():
    if not hasattr(world, "author"):
        try:
            world.author = Author.objects.all()[0]
        except IndexError:
            world.author = AuthorFactory()
            world.author.save()
    return world.author

def language():
    if not hasattr(world, "language"):
        try:
            world.language = Language.objects.all()[0]
        except IndexError:
            world.language = LanguageFactory()
            world.language.save()
    return world.language


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
    chapter.number = 0
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

@step(u'I should see a dialog show up')
def i_should_see_a_dialog_show_up(step):
    find(".dialog").is_displayed().should.be.true

@step(u'I should see on dialog "([^"]*)"')
def i_should_see_on_dialog(step, text):
    find(".dialog").text.should.contain(text)

@step(u'I should see option on dialog "([^"]*)"')
def i_should_see_option_on_dialog(step, option_text):
    label = ShortDom.label(option_text)
    label.should.be.ok
    ShortDom.element_for_label(label).should.be.ok

@step(u'I should see button on dialog "([^"]*)"')
def i_should_see_button_on_dialog(step, button_text):
    ShortDom.button(button_text, ".dialog").should.be.ok

@step(u'I should see checkbox on dialog "([^"]*)"')
def i_should_see_checkbox_on_dialog(step, checkbox_text):
    label = ShortDom.label(checkbox_text)
    label.should.be.ok
    checkbox = ShortDom.element_for_label(label)
    checkbox.should.be.ok
    checkbox.get_attribute("type").should.equal("checkbox")

@step(u'I click label on dialog "([^"]*)"')
def i_click_label_on_dialog(step, label_text):
    ShortDom.label(label_text, ".dialog").click()

@step(u'I click button on dialog "([^"]*)"')
def i_click_button_on_dialog(step, button_text):
    ShortDom.button(button_text, ".dialog").click()

@step(u'I should be reading book id "([^"]*)"')
def i_should_be_reading_book_id(step, book_id):
    book = Book.objects.get(pk=int(book_id))
    browser().current_url.should.contain(book.get_absolute_url())

@step(u'I should not see any dialog')
def i_should_not_see_any_dialog(step):
    find_all(".dialog").should_not.be.ok
