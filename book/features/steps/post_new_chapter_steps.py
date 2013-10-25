'''
Created on Sep 20, 2013

@author: antipro
'''
# -*- coding: utf-8 -*-
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.read_book_steps import i_click_on_a_book
from book.models.chapter_model import Chapter
from book.features.steps.favorite_book_steps import find_book_in_list
from book.features.steps.publish_new_book_steps import when_i_post_a_new_chapter_for_this_book

@step(u'I am reading a book')
def i_am_reading_a_book(step):
    i_visit_book_index_page(step)
    i_click_on_a_book(step)

@step(u'I submit a new book chapter')
def i_submit_a_new_book_chapter(step):
    world.old_total_chapters = get_total_chapters(int(world.choose_book_id))
    find("#post-new-chapter").click()
    when_i_post_a_new_chapter_for_this_book(step)

def get_total_chapters(book_id):
    db_commit()
    return Chapter.objects.filter(book_id=book_id).count()

def check_new_chapter_content():
    chapter = find("#chapter")
    chapter.find("h2 span.number").text.should.equal(str(world.old_total_chapters + 1))
    chapter.find("h2").text.should.contain("New chapter title")
    chapter.find(".content").text.should.contain("New chapter content")

@step(u'I see new chapter was posted')
def i_see_new_chapter_was_posted(step):
    find(".notifications").text.should.contain("New chapter was posted successfully.")
    i_am_reading_a_book(step)
    get_total_chapters(int(world.choose_book_id)).should.be.equal(world.old_total_chapters + 1)
    check_new_chapter_content()

@step(u'other people can read this chapter')
def other_people_can_read_this_chapter(step):
    logout_current_user()
    login_another_user(step)
    i_visit_book_index_page(step)
    find_book_in_list(world.choose_book_id).should_has_class("unread")
    i_click_on_a_book(step)
    last_page_link(".chapters_pagination").get_attribute('href').should.contain('?page=%s' % (world.old_total_chapters + 1))

@step(u'my posted chapter was increased')
def my_posted_chapter_was_increased(step):
    default_user().book_profile.chapters_count.should.equal(world.user_total_chapter_before_post + 1)
