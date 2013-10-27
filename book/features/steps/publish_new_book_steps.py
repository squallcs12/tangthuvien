'''
Created on Sep 24, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.index_steps import i_visit_book_index_page
import os
from book.models.book_model import Book

@step(u'When I publish a new book')
def when_i_publish_a_new_book(step):
    i_visit_book_index_page(step)
    find("#new-book").click()
    publish_book_form = find("#new-book-form")
    fill_new_book_form(publish_book_form, "Book title")
    publish_book_form.find("button[type='submit']").click()

def fill_new_book_form(form, book_title):
    form.find("[name='title']").send_keys(book_title)
    form.find("[name='cover']").send_keys(os.path.join(settings.MEDIA_ROOT, "books/covers/1278231576904.jpg"))
    form.find("[name='description']").fillin("Book description")

    form.find("[name='author']").select("-create-new-")
    fill_new_book_form.n += 1
    time.sleep(0.5)
    author_form = find("#new-author-form")
    author_form.find("[name='author-name']").send_keys("New author %s" % fill_new_book_form.n)
    author_form.find("[type='submit']").click()
    until(lambda: len(find_all(".modal-scrollable")) == 0, timeout=5)
    
    form.find("[name='ttv_type']").select("-create-new-")
    time.sleep(0.5)
    type_form = find("#new-type-form")
    fill_new_book_form.n += 1
    type_form.find("[name='type-name']").send_keys("New type %s" % fill_new_book_form.n)
    type_form.find("[type='submit']").click()
    until(lambda: len(find_all(".modal-scrollable")) == 0, timeout=5)
fill_new_book_form.n = 0

@step(u'Then I see a book was published')
def then_i_see_a_book_was_published(step):
    find(".notifications").text.should.contain("New book was published successfully.")

@step(u'And I was on the post new chapter page')
def and_i_was_on_the_post_new_chapter_page(step):
    browser().current_url.should.contain("post_new_chapter")

def get_book_title_list():
    title_links = find_all("#books .book a.title")
    return [link.text for link in title_links]

@step(u'And the book was not listed yet')
def and_the_book_was_not_listed_yet(step):
    i_visit_book_index_page(step)
    get_book_title_list().should_not.contain("Book title")
    browser().back()

def current_book_id():
    return int(browser().current_url.split('/').pop())

def current_book():
    db_commit()
    return Book.objects.get(pk=current_book_id())

@step(u'When I post a new chapter for this book')
def when_i_post_a_new_chapter_for_this_book(step):
    new_chapter_form = find("#new-chapter-form")
    new_chapter_form.find("input[name='title']").send_keys("New chapter title")
    new_chapter_form.find("input[name='number']").send_keys(str(current_book().chapters_count + 1))
    new_chapter_form.find("textarea[name='content']").fillin("New chapter content")

    new_chapter_form.find("select[name='chapter_type']").select("chapter-type-0")
    world.user_total_chapter_before_post = default_user().book_profile.chapters_count
    new_chapter_form.find("button[type='submit']").click()

@step(u'Then I see that book was listed')
def then_i_see_that_book_was_listed(step):
    i_visit_book_index_page(step)
    get_book_title_list().should.contain("Book title")
