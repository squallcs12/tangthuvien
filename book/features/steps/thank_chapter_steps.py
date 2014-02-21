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

@step(u'I see chapter thank count')
def i_see_chapter_thank_count(step):
    world.chapter_thank_count = get_thank_count()

@step(u'I can thank the poster for this chapter')
def i_can_thank_the_poster_for_this_chapter(step):
    get_thank_button().get_attribute('class').should_not.contain('btn-disable')

@step(u'I thank the poster for this chapter')
def i_thank_the_poster_for_this_chapter(step):
    get_thank_button().click()

@step(u'I see the chapter thank was increased')
def i_see_the_chapter_thank_was_increased(step):
    get_thank_count().should.equal(world.chapter_thank_count + 1)
    world.chapter_thank_count = world.chapter_thank_count + 1

@step(u'I can not thank the poster')
def i_can_not_thank_the_poster(step):
    get_thank_button().get_attribute('class').should.contain('btn-disable')

@step(u'I still see thank number not change after increasing')
def i_still_see_thank_number_not_change_after_increasing(step):
    get_thank_count().should.equal(world.chapter_thank_count)
