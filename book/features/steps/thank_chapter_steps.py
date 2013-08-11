# -*- coding: utf-8 -*-
'''
Created on Aug 3, 2013

@author: antipro
'''
from lettuce import step
from lettuce_setup.function import *

def get_thank_count():
    return int(find("#chapter-thank .count").text)

def get_thank_button():
    return find("#chapter-thank .thank-button")

@step(u'And I see chapter thank count')
def and_i_see_chapter_thank_count(step):
    world.chapter_thank_count = get_thank_count()

@step(u'And I can thank the poster for this chapter')
def and_i_can_thank_the_poster_for_this_chapter(step):
    get_thank_button().get_attribute('class').should_not.contain('disabled')

@step(u'When I thank the poster for this chapter')
def when_i_thank_the_poster_for_this_chapter(step):
    get_thank_button().click()

@step(u'Then I see the chapter thank was increased')
def then_i_see_the_chapter_thank_was_increased(step):
    get_thank_count().should.equal(world.chapter_thank_count + 1)
    world.chapter_thank_count = world.chapter_thank_count + 1

@step(u'And I can not thank the poster')
def and_i_can_not_thank_the_poster(step):
    get_thank_button().get_attribute('class').should.contain('disabled')

@step(u'Then I still see thank number not change after increasing')
def then_i_still_see_thank_number_not_change_after_increasing(step):
    get_thank_count().should.equal(world.chapter_thank_count)
