# -*- coding: utf-8 -*-
'''
Created on Jul 27, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.factories.book_factory import BookFactory
from book.features.factories.chapter_factory import ChapterFactory
from book.features.factories.chapter_type_factory import ChapterTypeFactory
from book.features.factories.category_factory import CategoryFactory
import random
from book.models.category_model import Category

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
    'truncate table book_profile;',
    'SET foreign_key_checks = 1;', ]
    for query in queries:
        execute_sql(query)

TOTAL_BOOK_WILL_BE_CREATED = 55

def create_book_list():
    clean_book_tables()
    world.book_created = True
    world.book_list = []

    chappter_types = []
    chappter_type = ChapterTypeFactory()
    chappter_type.save()
    chappter_types.append(chappter_type)
    for i in range(0, TOTAL_BOOK_WILL_BE_CREATED):  # @UnusedVariable
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

    for i in range(0, 4):
        category = CategoryFactory()
        category.save()
        assert isinstance(category, Category)
        for book in world.book_list:
            if random.randint(0, 1):
                category.books.add(book)

@step(u'I visit book index page')
def i_visit_book_index_page(step):
    visit('/books')

@step(u'Then I see list of books')
def then_i_see_list_of_books(step):
    check_title('List of books')
    [settings.BOOK_LIST_ITEM_COUNT, TOTAL_BOOK_WILL_BE_CREATED % settings.BOOK_LIST_ITEM_COUNT]\
        .should.contain(len(find_all("#books .book")))

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
    compare_list_item_ids(1, 2, "#books .book").should.be.false

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

def choose_category_filter(name):
    find(".categories_filters .bootstrap-tagsinput input").send_keys('c')
    find(".typeahead.dropdown-menu").find_element_by_link_text(name).click()
    world.current_url = browser().current_url


@step(u'When I choose a book category')
def when_i_choose_a_book_category(step):
    choose_category_filter("category-0")

@step(u'And I see the loading animation')
def and_i_see_the_loading_animation(step):
    find(".modal-backdrop")

@step(u'the loading animation finished')
def the_loading_animation_finished(step):
    until(lambda : len(find_all(".modal-backdrop")) == 0)

@step(u'Then I see the url was changed')
def then_i_see_the_url_was_changed(step):
    world.current_url.should_not.equal(browser().current_url)

@step(u'And I see only books in that category were listed')
def and_i_see_only_books_in_that_category_were_listed(step):
    for book in find_all("#books .book"):
        book.text.should.contain('category-0')

@step(u'When I choose one more book category')
def when_i_choose_one_more_book_category(step):
    choose_category_filter("category-1")

@step(u'Then I see only books in those categories was listed')
def then_i_see_only_books_in_those_categories_was_listed(step):
    for book in find_all("#books .book"):
        book.text.should.contain('category-0')
        book.text.should.contain('category-1')

@step(u'When I clear selected book categories')
def when_i_clear_selected_book_categories(step):
    for span in find(".categories_filters").find_all(".tag span"):
        span.click()

@step(u'Then I see all the books were listed')
def then_i_see_all_the_books_were_listed(step):
    save_list_item_ids(-1, "#books .book")
    compare_list_item_ids(1, -1, "#books .book").should.be.true

@step(u'And I see the books still there after reload the page')
def and_i_see_the_books_still_there_after_reload_the_page(step):
    save_list_item_ids('x', "#books .book")
    when_i_reload_the_page(step)
    save_list_item_ids('y', "#books .book")
    compare_list_item_ids('x', 'y', "#books .book").should.be.true
