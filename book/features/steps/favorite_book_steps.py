# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.read_book_steps import i_click_on_a_book, \
    i_go_to_last_chapter
from book.features.steps.upload_book_attachments_steps import read_book_by_id
from book.models.chapter_model import Chapter
from book.models.book_model import Book


@step(u'I am reading a book')
@step(u'I read a book$')
def i_read_a_book(step):
    i_visit_book_index_page(step)
    i_click_on_a_book(step)
    if len(find_all("#read_book")):
        find("#read_book").click()

def mark_as_favorite_button():
    return find("#favorite_book")

@step(u'I see the mark-as-favorite button')
def i_see_the_mark_as_favorite_button(step):
    mark_as_favorite_button().get_attribute('favorite').should.equal('no')

@step(u'I click on mark-as-favorite button')
def i_click_on_mark_as_favorite_button(step):
    mark_as_favorite_button().click()
    until(lambda: mark_as_favorite_button().get_attribute('favorite') == 'yes', 3)

@step(u'the book was mark as my favorite book')
def the_book_was_mark_as_my_favorite_book(step):
    favorite_count = eval_sql("SELECT count(*) from book_favorite WHERE user_id = %s" % default_user().id)
    favorite_count.should.equal(1)

@step(u'I visit favorite-books manager page')
def i_visit_favorite_books_manager_page(step):
    visit_by_view_name('favorite_books')

@step(u'I see the book was listed there')
def i_see_the_book_was_listed_there(step):
    for book in find_all("#books.favorite .book"):
        if book.get_attribute("item_id") == world.book_id:
            return
    raise Exception("Book was not listed in favorite list")

@step(u'I read the last chapter of the book')
def i_read_the_last_chapter_of_the_book(step):
    read_book_by_id(world.book_id)
    find("#chapters_list a:last-child").click()

@step(u'a new chapter was posted to the book')
def a_new_chapter_was_posted_to_the_book(step, book=None):
    if book is None:
        book = Book.objects.get(pk=int(world.book_id))
    Chapter.objects.create(
        user=default_user(),
        book=book,
        title="New posted chapter",
        content="New posted chapter content",
        number=book.chapters_count + 1
    )

@step(u'I see that book marked as unread on favorite list')
def i_see_that_book_marked_as_unread_on_favorite_list(step):
    i_visit_favorite_books_manager_page(step)
    find("#books .book[item_id='%s']" % world.book_id).get_attribute('unread').should.equal('yes')

def find_book_in_list(book_id):
    return find("#books .book[item_id='%s']" % book_id)

@step(u'I remove the book from favorite list')
def i_remove_the_book_from_favorite_list(step):
    find_book_in_list(world.book_id).find("input[type='checkbox']").click()
    find("#unfavorite_books").click()
    i_read_the_last_chapter_of_the_book(step)

@step(u'I see the book was marked as favorite')
def i_see_the_book_was_marked_as_favorite(step):
    mark_as_favorite_button().get_attribute('favorite').should.equal('yes')

@step(u'I see the book was not marked as favorite')
def i_see_the_book_was_not_marked_as_favorite(step):
    mark_as_favorite_button().get_attribute('favorite').should.equal('no')
