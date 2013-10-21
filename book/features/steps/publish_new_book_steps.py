'''
Created on Sep 24, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.index_steps import i_visit_book_index_page
import os
from tangthuvien import settings

@step(u'When I publish a new book')
def when_i_publish_a_new_book(step):
    i_visit_book_index_page(step)
    find("#new-book").click()

    publish_book_form = find("#new-book-form")
    publish_book_form.find("[name='title']").send_keys("Book title")
    publish_book_form.find("[name='cover']").send_keys(os.path.join(settings.MEDIA_ROOT, "books/covers/1278231576904.jpg"))
    publish_book_form.find("[name='description']").fillin("Book description")
    publish_book_form.find("[name='author']").select("Author 0")
    publish_book_form.find("[name='ttv_type']").select("book-type-0")
    publish_book_form.find("button[type='submit']").click()

@step(u'Then I a book was published')
def then_i_a_book_was_published(step):
    find(".notifications").text.should.contain("New book was published successfully.")

@step(u'And I was on the post new chapter page')
def and_i_was_on_the_post_new_chapter_page(step):
    browser().current_url.should.contain("post_new_chapter")

def get_book_title_list():
    title_links = find_all("#books .row .panel .panel-heading h4 a")
    return [link.text for link in title_links]

@step(u'And the book was not listed yet')
def and_the_book_was_not_listed_yet(step):
    i_visit_book_index_page(step)
    get_book_title_list().should_not.contain("Book title")
    browser().back()

@step(u'When I post a new chapter for this book')
def when_i_post_a_new_chapter_for_this_book(step):
    new_chapter_form = find("#new-chapter-form")
    new_chapter_form.find("input[name='title']").send_keys("New chapter title")
    new_chapter_form.find("input[name='number']").send_keys("11")
    new_chapter_form.find("textarea[name='content']").fillin("New chapter content")

    new_chapter_form.find("select[name='chapter_type']").select("chapter-type-0")
    world.user_total_chapter_before_post = default_user().book_profile.chapters_count
    new_chapter_form.find("button[type='submit']").click()

@step(u'Then I see that book was listed')
def then_i_see_that_book_was_listed(step):
    i_visit_book_index_page(step)
    get_book_title_list().should.contain("Book title")
