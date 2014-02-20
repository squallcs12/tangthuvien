'''
Created on Oct 23, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.publish_new_book_steps import fill_new_book_form, \
    get_book_title_list
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.read_book_steps import i_go_to_last_chapter, \
    see_the_last_chapter, see_the_second_chapter
from book.features.steps.upload_book_attachments_steps import read_book_by_id
from book.models.book_model import Book

@step(u'And I press "([^"]*)"')
def and_i_press(step, text):
    browser().find_element_by_link_text(text).click()

@step(u'And I fill the book information page')
def and_i_fill_the_book_information_page(step, book_title="Copy book title"):
    copy_book_form = find("#copy-book-form")
    fill_new_book_form(copy_book_form, book_title)
    copy_book_form.find("input[name='thread_url']").send_keys("http://www.tangthuvien.vn/forum/showthread.php?t=50129")
    copy_book_form.find("button[type='submit']").click()

@step(u'Then I see the copying was processed')
def then_i_see_the_copying_was_processed(step):
    world.copied_book_id = browser().current_url.split('?')[0].split('/').pop()  # last number in the url
    find("#process_bar.progress .progress-bar")

@step(u'When the process is finished')
def when_the_process_is_finished(step):
    until(lambda: find("#process_bar.progress .progress-bar").text == '100%', timeout=20)

@step(u'Then I see the whole book was copied')
def then_i_see_the_whole_book_was_copied(step):
    db_commit()
    book = Book.objects.get(pk=world.copied_book_id)
    book.chapter_set.all()[1].delete()
    copy_log = book.copy
    copy_log.last_post = 1
    copy_log.save()
    i_visit_book_index_page(step)
    get_book_title_list().should.contain("Copy book title")
    browser().find_element_by_link_text("Copy book title").click()

@step(u'And I can not copy this thread again')
def and_i_can_not_copy_this_thread_again(step):
    i_visit_book_index_page(step)
    browser().find_element_by_link_text("Copy book").click()
    and_i_fill_the_book_information_page(step, "Copy book title 2")
    find(".notifications").text.should.contain(trans(u"The book is already copied to this site."))

@step(u'When I visit the copied book')
def when_i_visit_the_copied_book(step):
    read_book_by_id(world.copied_book_id)

@step(u'Then I can sync the new posted chapter from main-site of this book')
def then_i_can_sync_the_new_posted_chapter_from_main_site_of_this_book(step):
    len(find_all("#sync-copy-book")).should_not.equal(0)

@step(u'When I sync the new posted chapter')
def when_i_sync_the_new_posted_chapter(step):
    find("#sync-copy-book").click()

@step(u'Then I see only new posted chapter was copied')
def then_i_see_only_new_posted_chapter_was_copied(step):
    read_book_by_id(world.copied_book_id)
    i_go_to_last_chapter(step)
    see_the_second_chapter(step)

@step(u'I visit the redirect page for copied thread id')
def i_visit_the_redirect_page_for_copied_thread_id(step):
    visit_by_view_name("thread_redirect_view", kwargs={"tid": 50129})

@step(u'I was redirected to the reading page of copied book')
def i_was_redirected_to_the_reading_page_of_copied_book(step):
    until(lambda: len(find_all("#sync-copy-book")).should_not.equal(0))
