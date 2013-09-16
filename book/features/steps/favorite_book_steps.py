# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.read_book_steps import i_click_on_a_book, \
    i_go_to_last_chapter
from book.models.chapter_model import Chapter
from book.models.book_model import Book
from book.models import ChapterType

@step(u'I read a book')
def i_read_a_book(step):
    i_visit_book_index_page(step)
    i_click_on_a_book(step)
    world.favorite_book_id = find("#book").get_attribute("item_id")  # @UnusedVariable

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
        if book.get_attribute("item_id") == world.favorite_book_id:
            return
    raise Exception("Book was not listed in favorite list")

@step(u'I read the last chapter of the book')
def i_read_the_last_chapter_of_the_book(step):
    visit_by_view_name('book_read_short', kwargs={'book_id':world.favorite_book_id})
    i_go_to_last_chapter(step)

@step(u'a new chapter was posted to the book')
def a_new_chapter_was_posted_to_the_book(step):
    Chapter.objects.create(
        user=default_user(),
        book=Book.objects.get(pk=int(world.favorite_book_id)),
        title="New posted chapter",
        content="New posted chapter content",
        chapter_type=ChapterType.objects.all()[0],
        number=eval_sql("SELECT MAX(number) FROM book_chapter WHERE book_id=%s" % world.favorite_book_id) + 1
    )

@step(u'I see that book marked as unread on favorite list')
def i_see_that_book_marked_as_unread_on_favorite_list(step):
    i_visit_favorite_books_manager_page(step)
    find("#books .book[item_id='%s']" % world.favorite_book_id).get_attribute('unread').should.equal('yes')


@step(u'I remove the book from favorite list')
def i_remove_the_book_from_favorite_list(step):
    find("#books .book[item_id='%s'] .panel" % world.favorite_book_id).click()
    find("#unfavorite_books").click()
    i_read_the_last_chapter_of_the_book(step)

@step(u'I see the book was marked as favorite')
def i_see_the_book_was_marked_as_favorite(step):
    mark_as_favorite_button().get_attribute('favorite').should.equal('yes')

@step(u'I see the book was not marked as favorite')
def i_see_the_book_was_not_marked_as_favorite(step):
    mark_as_favorite_button().get_attribute('favorite').should.equal('no')
