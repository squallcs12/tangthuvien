'''
Created on Sep 24, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.index_steps import i_visit_book_index_page
import os
from book.models.book_model import Book

@step(u'I see a book was published')
def i_see_a_book_was_published(step):
    find(".notifications").text.should.contain(trans(u"New book was published successfully."))

def get_book_title_list():
    title_links = find_all("#books .book a.title")
    return [link.text for link in title_links]

@step(u'the book was not listed yet')
def the_book_was_not_listed_yet(step):
    i_visit_book_index_page(step)
    get_book_title_list().should_not.contain("Book title")
    browser().back()

@step(u'I post a new chapter for this book')
def i_post_a_new_chapter_for_this_book(step):
    from book.features.steps.post_new_chapter_steps import i_fill_title_for_this_chapter, \
        i_enter_chapter_content, \
        i_fill_the_next_chapter_number_for_this_chapter, \
        i_select_language_for_this_chapter, \
        i_see_the_post_new_chapter_form
    i_see_the_post_new_chapter_form(step)
    i_fill_title_for_this_chapter(step, "New book chapter")
    i_enter_chapter_content(step, "New book chapter content")
    i_fill_the_next_chapter_number_for_this_chapter(step)
    i_select_language_for_this_chapter(step)
    i_click_on(step, "Post chapter")

@step(u'I see that book "([^"]*)" was listed')
def i_see_that_book_was_listed(step, title):
    i_visit_book_index_page(step)
    get_book_title_list().should.contain(title)

@step(u'I fill in book title "([^"]*)"')
def i_fill_in_book_title(step, title):
    world.book_form.find("input[name='title']").send_keys(title)

@step(u'I fill in book description')
def i_fill_in_book_description(step):
    world.book_form.find("textarea[name='description']").fillin("Book description")

@step(u'I select image for book cover')
def i_select_image_for_book_cover(step):
    world.book_form.find("input[name='cover']").send_keys(os.path.join(settings.MEDIA_ROOT, "books/covers/1278231576904.jpg"))

@step(u'I select book author')
def i_select_book_author(step):
    try:
        world.book_form.find("select[name='author']").select("Author 1")
    except:
        i_create_new_author_of_this_book(step)

@step(u'I create new author of this book')
def i_create_new_author_of_this_book(step):
    world.book_form.find("select[name='author']").select("-create-new-")
    time.sleep(0.5)
    author_form = find("#new-author-form")
    author_form.find("input[name='author-name']").send_keys("Author 1")
    author_form.find("button[type='submit']").click()
    until(lambda: author_form.is_displayed().should.be.false, timeout=5)

@step(u'I select book categories')
def i_select_book_categories(step):
    for category in ['category-1', 'category-2']:
        world.book_form.find("select[name='categories']").select(category)

@step(u'I select languages')
def i_select_languages(step):
    for language in ['language-1', 'language-2']:
        world.book_form.find("select[name='languages']").select(language)

@step(u'I submit the publish form')
def i_submit_the_publish_form(step):
    world.book_form.find("button[type='submit']").click()

@step(u'I see the new book form')
def i_see_the_new_book_form(step):
    world.book_form = find("#new-book-form")
