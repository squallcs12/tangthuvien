'''
Created on Oct 23, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.publish_new_book_steps import fill_new_book_form, \
    get_book_title_list
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.read_book_steps import i_go_to_last_chapter, \
    see_the_last_chapter

@step(u'And I press "([^"]*)"')
def and_i_press(step, text):
    browser().find_element_by_link_text(text).click()

@step(u'And I fill the book information page')
def and_i_fill_the_book_information_page(step):
    copy_book_form = find("#copy-book-form")
    fill_new_book_form(copy_book_form, "Copy book title")
    copy_book_form.find("input[name='thread_url']").send_keys("http://www.tangthuvien.vn/forum/showthread.php?t=50129")
    copy_book_form.find("button[type='submit']").click()

@step(u'Then I see the copying was processed')
def then_i_see_the_copying_was_processed(step):
    find("#process_bar.progress .progress-bar")

@step(u'When the process is finished')
def when_the_process_is_finished(step):
    until(lambda: find("#process_bar.progress .progress-bar").text == '100%')

@step(u'Then I see the whole book was copied')
def then_i_see_the_whole_book_was_copied(step):
    i_visit_book_index_page(step)
    get_book_title_list().should.contain("Copy book title")
    browser().find_element_by_link_text("Copy book title").click()
    i_go_to_last_chapter(step)
    see_the_last_chapter(step)

