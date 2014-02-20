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
import subprocess
from tangthuvien import settings as st
from django.contrib.auth.models import User, Group
from book.models.book_model import Book

@step(u'I visit book index page')
def i_visit_book_index_page(step):
    visit('/books')

@step(u'I see list of books')
def i_see_list_of_books(step):
    check_title(trans(u'List of books'))
    range(0, settings.BOOK_LIST_ITEM_COUNT + 1).should.contain(len(find_all("#books .book")))

@step(u'I was at the first page of listing')
def i_was_at_the_first_page_of_listing(step):
    first_page_link(".books_pagination").should_be_temp_link()
    save_list_item_ids(1, "#books .book")

    current_page = current_page_link(".books_pagination")
    current_page.should_be_temp_link()
    int(current_page.text).should.equal(1)

@step(u'I go to the next page')
def i_go_to_the_next_page(step):
    next_page_link(".books_pagination").click()

@step(u'those books difference from the first page')
def those_books_difference_from_the_first_page(step):
    save_list_item_ids(2, "#books .book")
    compare_list_item_ids(1, 2, "#books .book").should.be.false

@step(u'I was at the second page of listing')
def i_was_at_the_second_page_of_listing(step):
    current_page = current_page_link(".books_pagination")
    int(current_page.text).should.equal(2)

@step(u'I go to the last page')
def i_go_to_the_last_page(step):
    last_page_link(".books_pagination").click()

@step(u'those books difference from the other pages')
def those_books_difference_from_the_other_pages(step):
    last_page_number = int(current_page_link(".books_pagination").text)
    compare_list_item_ids(1, last_page_number, "#books .book").should.be(False)
    compare_list_item_ids(2, last_page_number, "#books .book").should.be(False)

@step(u'I was at the last page of listing')
def i_was_at_the_last_page_of_listing(step):
    last_page_link(".books_pagination").should_be_temp_link()

    last_page_number = int(current_page_link(".books_pagination").text)
    save_list_item_ids(last_page_number, "#books .book")

def choose_category_filter(name):
    world.current_url = browser().current_url
    find(".categories_filters .bootstrap-tagsinput input").send_keys('c')
    until(lambda: find(".typeahead.dropdown-menu").find_element_by_link_text(name))
    find(".typeahead.dropdown-menu").find_element_by_link_text(name).click()


@step(u'I choose a book category')
def i_choose_a_book_category(step):
    choose_category_filter("category-0")

@step(u'the loading animation finished')
def the_loading_animation_finished(step):
    until(lambda : len(find_all(".modal-backdrop")) == 0)

@step(u'I see the url was changed')
def i_see_the_url_was_changed(step):
    world.current_url.should_not.equal(browser().current_url)

@step(u'I see only books in that category were listed')
def i_see_only_books_in_that_category_were_listed(step):
    for book in find_all("#books .book"):
        book.text.should.contain('category-0')
    save_list_item_ids(-3, "#books .book")

@step(u'I choose one more book category')
def i_choose_one_more_book_category(step):
    choose_category_filter("category-1")

@step(u'I see only books in those categories was listed')
def i_see_only_books_in_those_categories_was_listed(step):
    for book in find_all("#books .book"):
        book.text.should.contain('category-0')
        book.text.should.contain('category-1')

@step(u'I clear selected book categories')
def i_clear_selected_book_categories(step):
    for span in find(".categories_filters").find_all(".tag span"):
        span.click()

@step(u'I see all the books were listed')
def i_see_all_the_books_were_listed(step):
    save_list_item_ids(-1, "#books .book")
    compare_list_item_ids(1, -1, "#books .book").should.be.true

@step(u'I see the books still there after reload the page')
def i_see_the_books_still_there_after_reload_the_page(step):
    save_list_item_ids('x', "#books .book")
    when_i_reload_the_page(step)
    save_list_item_ids('y', "#books .book")
    compare_list_item_ids('x', 'y', "#books .book").should.be.true


@step(u'I click browser back button')
def i_click_browser_back_button(step):
    browser().back()

@step(u'I see the previous books was listed')
def i_see_the_previous_books_was_listed(step):
    save_list_item_ids(-4, "#books .book")
    compare_list_item_ids(-3, -4, "#books .book")
