'''
Created on Oct 25, 2013

@author: antipro
'''
from lettuce_setup.function import *
from book.features.steps.index_steps import i_visit_book_index_page

@step(u'I change the reading section font face and font size')
def i_change_the_reading_section_font_face_and_font_size(step):
    find("#read_config .config").click()
    config_div = find("#config-modal")
    config_div.find("[name='font_family']").select("Arial")
    config_div.find("[name='font_size']").select("20px")
    config_div.find("[type='submit']").click()


@step(u'I see the configuration of readind section is applied')
def i_see_the_configuration_of_readind_section_is_applied(step):
    find("#chapter .content").value_of_css_property('font-size').should.equal('20px')
    find("#chapter .content").value_of_css_property('font-family').should.equal('Arial')

@step(u'I read another book')
def i_read_another_book(step):
    i_visit_book_index_page(step)
    book_div = find_all("#books .book")[1]
    book_div.find("a.title").click()
