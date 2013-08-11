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
    book_div = find("#books .book")
    world.choose_book_id = book_div.get_attribute('item_id')
    book_div.find("a.title").click()

@step(u'I see the book title and description')
def i_see_the_book_title_and_description(step):
    find("#book h4.title").text.should_not.be.empty
    find("#book div.description").text.should_not.be.empty

@step(u'And I see the author name and information')
def and_i_see_the_author_name_and_information(step):
    find("#author h4.title").text.should_not.be.empty
    find("#author div.information").text.should_not.be.empty

def check_chapter(number):
    find("#chapter .number").text.should.equal(str(number))
    find("#chapter .content").text.should_not.be.empty

@step(u'And I see the first chapter')
def and_i_see_the_first_chapter(step):
    check_chapter(1)

@step(u'When I go to next chapter')
def when_i_go_to_next_chapter(step):
    next_page_link("#pagination").click()

@step(u'see the second chapter')
def see_the_second_chapter(step):
    check_chapter(2)

@step(u'When I choose a random chapter from selection box')
def when_i_choose_a_random_chapter_from_selection_box(step):
    world.random_chapter_choose = random.randint(3, 7)
    find("#pagination .chapter-list option[value='%s']" % world.random_chapter_choose).click()

@step(u'see a random chapter')
def see_a_random_chapter(step):
    check_chapter(world.random_chapter_choose)

@step(u'And I click on the previous book')
def and_i_click_on_the_previous_book(step):
    find("#books .book[item_id='%s'] a.title" % world.choose_book_id).click()

@step(u'see the last random chapter')
def see_the_last_random_chapter(step):
    see_a_random_chapter(step)

@step(u'When I go to last chapter')
def when_i_go_to_last_chapter(step):
    last_page_link("#pagination").click()

@step(u'see the last chapter')
def see_the_last_chapter(step):
    last_page_link("#pagination").tag_name.should_not.equal('a')
