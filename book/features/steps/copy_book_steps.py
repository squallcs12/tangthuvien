'''
Created on Oct 23, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.publish_new_book_steps import get_book_title_list
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.upload_book_attachments_steps import read_book_by_id
from book.models.book_model import Book

@step(u'I see the copying was processed')
def i_see_the_copying_was_processed(step):
    db_commit()
    world.copied_book_id = browser().current_url.split('?')[0].split('/').pop()  # last number in the url
    find("#process_bar.progress .progress-bar")

@step(u'the process is finished')
def the_process_is_finished(step):
    until(lambda: find("#process_bar.progress .progress-bar").text == '100%', timeout=20)

@step(u'I see the whole book was copied')
def i_see_the_whole_book_was_copied(step):

    # delete last chapter from copying
    db_commit()
    book = Book.objects.get(pk=world.copied_book_id)

    world.copied_chapters_count = book.chapter_set.all().count()
    skip = True
    for chapter in book.chapter_set.all():
        if skip:
            skip = False
            continue
        chapter.delete()

    copy_log = book.copy
    copy_log.last_post = 2  # because in this thread, first chapter is in 2nd post
    copy_log.save()

    i_visit_book_index_page(step)
    get_book_title_list().should.contain("Copy book title")
    link("Copy book title").click()

@step(u'I visit the copied book')
def i_visit_the_copied_book(step):
    read_book_by_id(world.copied_book_id)

@step(u'I can sync the new posted chapter from main-site of this book')
def i_can_sync_the_new_posted_chapter_from_main_site_of_this_book(step):
    len(find_all("#sync-copy-book")).should_not.equal(0)

@step(u'I sync the new posted chapter')
def i_sync_the_new_posted_chapter(step):
    find("#sync-copy-book").click()

@step(u'I see only new posted chapter was copied')
def i_see_only_new_posted_chapter_was_copied(step):
    db_commit()
    book = Book.objects.get(pk=world.copied_book_id)
    book.chapter_set.all().count().should.equal(world.copied_chapters_count)

@step(u'I visit the redirect page for copied thread id')
def i_visit_the_redirect_page_for_copied_thread_id(step):
    visit_by_view_name("thread_redirect_view", kwargs={"thread_id": 50129})

@step(u'I was redirected to the reading page of copied book')
def i_was_redirected_to_the_reading_page_of_copied_book(step):
    until(lambda: len(find_all("#sync-copy-book")).should_not.equal(0))

@step(u'I see the copy book form')
def i_see_the_copy_book_form(step):
    world.book_form = find("#copy-book-form")

@step(u'I fill in book source thread page "([^"]*)"')
def i_fill_in_book_source_thread_page(step, thread_url):
    world.book_form.find("input[name='thread_url']").send_keys(thread_url)
