# -*- coding: utf-8 -*-
'''
Created on Jul 29, 2013

@author: antipro
'''
from lettuce import step
from lettuce_setup.function import *  # @UnusedWildImport
import random

@step(u'I click on a book')
def i_click_on_a_book(step):
    book_div = find_all("#books .book").pop()
    world.choose_book_id = book_div.get_attribute('item_id')
    book_div.find("a.title").click()

@step(u'I see the book title and description')
def i_see_the_book_title_and_description(step):
    find("#book .panel-heading").text.should_not.be.empty
    find("#book .panel-body").text.should_not.be.empty

@step(u'I see the author name and information')
def i_see_the_author_name_and_information(step):
    find("#author .panel-heading").text.should_not.be.empty
    find("#author .panel-body").text.should_not.be.empty

def check_chapter(number):
    find("#chapter .number").text.should.equal(str(number))
    find("#chapter .content").text.should_not.be.empty

@step(u'And I see the first chapter')
def and_i_see_the_first_chapter(step):
    check_chapter(1)

@step(u'I go to next chapter')
def i_go_to_next_chapter(step):
    find(".chapters_pagination").find_all(".pagination a").pop().click()

@step(u'see the second chapter')
def see_the_second_chapter(step):
    check_chapter(2)

@step(u'I choose a random chapter from selection box')
def i_choose_a_random_chapter_from_selection_box(step):
    world.random_chapter_choose = random.randint(3, 7)
    find(".chapters_pagination .chapter-list option[value='%s']" % world.random_chapter_choose).click()

@step(u'see a random chapter')
def see_a_random_chapter(step):
    check_chapter(world.random_chapter_choose)

@step(u'I click on the previous book')
def i_click_on_the_previous_book(step):
    find("#books .book[item_id='%s'] a.title" % world.choose_book_id).click()

@step(u'see the last random chapter')
def see_the_last_random_chapter(step):
    see_a_random_chapter(step)

@step(u'I go to last chapter')
def i_go_to_last_chapter(step):
    find_all(".chapters_pagination .chapter-list option").pop().click()

@step(u'see the last chapter')
def see_the_last_chapter(step):
    find_all(".chapters_pagination .pagination a").pop().should_be_temp_link()
