'''
Created on Aug 25, 2013

@author: antipro
'''
from lettuce_setup.function import *

@step(u'When I visit the homepage')
def when_i_visit_the_homepage(step):
    visit_by_view_name('homepage')

@step(u'And I change the style of website')
def and_i_change_the_style_of_website(step):
    find("#change_style_link").click()
    find("#style_menu").find_element_by_link_text("Readable").click()

@step(u'Then I see the style of website was changed')
def then_i_see_the_style_of_website_was_changed(step):
    browser().page_source.should.contain("/readable.css")

@step(u'Then I still see the style of website was keep as I changed')
def then_i_still_see_the_style_of_website_was_keep_as_i_changed(step):
    then_i_see_the_style_of_website_was_changed(step)
