# -*- coding: utf-8 -*-
'''
Created on Jul 27, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.factories.book_factory import BookFactory
from book.features.factories.chapter_factory import ChapterFactory
from book.features.factories.chapter_type_factory import ChapterTypeFactory

@before.each_feature
def before_book_feature(feature):
    if ('Book App ::' in feature.name) and \
        (not hasattr(world, 'book_created') or not world.book_created):
        create_book_list()

def clean_book_tables():
    '''
    Clean all book app table
    '''
    queries = ['SET foreign_key_checks = 0;',
    'truncate table book_author;',
    'truncate table book_book;',
    'truncate table book_book_categories;',
    'truncate table book_book_sites;',
    'truncate table book_booktype;',
    'truncate table book_category;',
    'truncate table book_chapter;',
    'truncate table book_chaptertype;',
    'truncate table book_type;',
    'truncate table book_userlog;',
    'truncate table book_chapterthank;',
    'truncate table book_chapterthanksummary;',
    'truncate table book_rating;',
    'truncate table book_ratinglog;',
    'truncate table book_favorite;',
    'SET foreign_key_checks = 1;', ]
    for query in queries:
        execute_sql(query)


def create_book_list():
    clean_book_tables()
    world.book_created = True
    world.book_list = []

    chappter_types = []
    chappter_type = ChapterTypeFactory()
    chappter_type.save()
    chappter_types.append(chappter_type)
    for i in range(0, 50):  # @UnusedVariable
        book = BookFactory()
        book.save()
        world.book_list.append(book)
        for i in range(1, 11):
            chapter = ChapterFactory()
            chapter.number = i
            chapter.book = book
            chapter.chapter_type = chappter_type
            chapter.user = book.user
            chapter.save()

@step(u'I visit book index page')
def i_visit_book_index_page(step):
    visit('/books')

@step(u'Then I see list of books')
def then_i_see_list_of_books(step):
    check_title('List of books')
    len(find_all("#books .book")).should.equal(10)

@step(u'And I was at the first page of listing')
def and_i_was_at_the_first_page_of_listing(step):
    first_page_link(".books_pagination").should_be_temp_link()
    save_list_item_ids(1, "#books .book")

    current_page = current_page_link(".books_pagination")
    current_page.should_be_temp_link()
    int(current_page.text).should.equal(1)

@step(u'When I go to the next page')
def when_i_go_to_the_next_page(step):
    next_page_link(".books_pagination").click()

@step(u'And those books difference from the first page')
def and_those_books_difference_from_the_first_page(step):
    save_list_item_ids(2, "#books .book")
    compare_list_item_ids(1, 2, "#books .book").should.be(False)

@step(u'And I was at the second page of listing')
def and_i_was_at_the_second_page_of_listing(step):
    current_page = current_page_link(".books_pagination")
    int(current_page.text).should.equal(2)

@step(u'When I go to the last page')
def when_i_go_to_the_last_page(step):
    last_page_link(".books_pagination").click()

@step(u'And those books difference from the other pages')
def and_those_books_difference_from_the_other_pages(step):
    last_page_number = int(current_page_link(".books_pagination").text)
    compare_list_item_ids(1, last_page_number, "#books .book").should.be(False)
    compare_list_item_ids(2, last_page_number, "#books .book").should.be(False)

@step(u'And I was at the last page of listing')
def and_i_was_at_the_last_page_of_listing(step):
    last_page_link(".books_pagination").should_be_temp_link()

    last_page_number = int(current_page_link(".books_pagination").text)
    save_list_item_ids(last_page_number, "#books .book")

