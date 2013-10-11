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

    publish_book_form = find("#publish_book_form")
    publish_book_form.find("name=['title']").send_keys("Book title")
    publish_book_form.find("name=['cover']").send_keys(os.path.join(settings.MEDIA_ROOT, "books/covers/1278231576904.jpg"))
    publish_book_form.find("name=['description']").send_keys("Book description")
    publish_book_form.find("name=['title']").send_keys("Book title")
    publish_book_form.find("name=['title']").send_keys("Book title")
    publish_book_form.find("name=['title']").send_keys("Book title")

@step(u'Then I see that book is listed')
def then_i_see_that_book_is_listed(step):
    assert False, 'This step must be implemented'
@step(u'Given I publish a number of books')
def given_i_publish_a_number_of_books(step):
    assert False, 'This step must be implemented'
@step(u'When I visit those book categories')
def when_i_visit_those_book_categories(step):
    assert False, 'This step must be implemented'
