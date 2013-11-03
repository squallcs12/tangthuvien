# -*- coding: utf-8 -*-
'''
Created on Aug 4, 2013

@author: antipro
'''
from lettuce import step
from lettuce_setup.function import *

def get_rate_button():
    return find_all("#book_rating .rate-star button")

@step(u'I see the book rating box')
def i_see_the_book_rating_box(step):
    find("#book_rating")

@step(u'I see the book rating result')
def i_see_the_book_rating_result(step):
    find("#book_rating .result")

@step(u'I see rating book button')
def i_see_rating_book_button(step):
    len(get_rate_button()).should.equal(5)

@step(u'I can not rate for the book')
def i_can_not_rate_for_the_book(step):
    for button in get_rate_button():
        button.get_attribute('disabled').should.equal('true')

@step(u'I can rate for the book')
def i_can_rate_for_the_book(step):
    for button in get_rate_button():
        button.get_attribute('disabled').should_not.equal('true')

@step(u'I rate (.*) star for the book')
def i_rate_star_for_the_book(step, number):
    find("#book_rating .rate-star-%s" % number).click()

@step(u'I see the book rating is (.*)')
def i_see_the_book_rating_is(step, number):
    try:
        find("#book_rating .average-result").text.should.equal(number)
    except:
        find("#book_rating .average-result").text.should.equal(number.replace('.', ','))

@step(u'I see the book rating count is (.*)')
def i_see_the_book_rating_count_is(step, number):
    find("#book_rating .rating-count").text.should.equal(number)
