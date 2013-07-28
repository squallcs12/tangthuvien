# -*- coding: utf-8 -*-
'''
Created on Jul 27, 2013

@author: antipro
'''
from lettuce import step, before, after
from lettuce_setup.function import *  # @UnusedWildImport
import pdb
from book.features.factories.book_factory import BookFactory

@before.each_feature
def before_book_feature(feature):
    if feature.name == 'Books page':
        create_book_list()
@after.each_feature
def after_book_feature(feature):
    if feature.name == 'Books page':
        delete_book_list()

def create_book_list():
    world.book_list = []
    for i in range(0, 50):  # @UnusedVariable
        book = BookFactory()
        book.save()
        world.book_list.append(book)

def delete_book_list():
    for book in world.book_list:
        book.ttv_type.delete()
        book.author.delete()
    world.book_list = []


@step(u'When I visit book index page')
def when_i_visit_book_index_page(step):
    visit("/books")

@step(u'Then I see list of books')
def then_i_see_list_of_books(step):
    check_title('List of books')
    len(find_all("#books .book")).should.equal(10)

@step(u'And I was at the first page of listing')
def and_i_was_at_the_first_page_of_listing(step):
    first_link = first_page_link("#pagination")
    first_link.tag_name.should_not.equal('a')
    save_list_item_ids(1, "#books .book")

    current_page = current_page_link("#pagination")
    current_page.tag_name.should_not.equal('a')
    int(current_page.text).should.equal(1)

@step(u'When I go to the next page')
def when_i_go_to_the_next_page(step):
    next_page_link("#pagination").click()

@step(u'And those books difference from the first page')
def and_those_books_difference_from_the_first_page(step):
    save_list_item_ids(2, "#books .book")
    compare_list_item_ids(1, 2, "#books .book").should.be(False)

@step(u'And I was at the second page of listing')
def and_i_was_at_the_second_page_of_listing(step):
    current_page = current_page_link("#pagination")
    int(current_page.text).should.equal(2)

@step(u'When I go to the last page')
def when_i_go_to_the_last_page(step):
    last_page_link("#pagination").click()

@step(u'And those books difference from the other pages')
def and_those_books_difference_from_the_other_pages(step):
    last_page_number = int(current_page_link("#pagination").text)
    compare_list_item_ids(1, last_page_number, "#books .book").should.be(False)
    compare_list_item_ids(2, last_page_number, "#books .book").should.be(False)

@step(u'And I was at the last page of listing')
def and_i_was_at_the_last_page_of_listing(step):
    last_link = last_page_link("#pagination")
    last_link.tag_name.should_not.equal('a')

    last_page_number = int(current_page_link("#pagination").text)
    save_list_item_ids(last_page_number, "#books .book")
