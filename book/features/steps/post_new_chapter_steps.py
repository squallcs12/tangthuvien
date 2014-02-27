'''
Created on Sep 20, 2013

@author: antipro
'''
# -*- coding: utf-8 -*-
from lettuce_setup.function import *  # @UnusedWildImport
from book.features.steps.general import *
from book.features.steps.index_steps import i_visit_book_index_page
from book.features.steps.favorite_book_steps import i_read_a_book
from book.models.chapter_model import Chapter
from book.features.steps.favorite_book_steps import find_book_in_list
from book.features.steps.publish_new_book_steps import i_post_a_new_chapter_for_this_book

@step(u'I am reading a book')
def i_am_reading_a_book(step):
    i_visit_book_index_page(step)
    i_read_a_book(step)

@step(u'I submit a new book chapter')
def i_submit_a_new_book_chapter(step):
    world.old_total_chapters = get_total_chapters(int(world.book_id))
    find("#post-new-chapter").click()
    i_post_a_new_chapter_for_this_book(step)

def get_total_chapters(book_id):
    db_commit()
    return Chapter.objects.filter(book_id=book_id).count()

@step(u'I see new chapter was posted')
def i_see_new_chapter_was_posted(step):
    find(".notifications").text.should.contain(trans(u"New chapter was posted successfully."))
    i_am_reading_a_book(step)
    get_total_chapters(int(world.book_id)).should.be.equal(world.old_total_chapters + 1)
    chapter = find("#chapter")
    chapter.find("h2 span.number").text.should.equal(str(world.old_total_chapters + 1))

@step(u'other people can read this chapter')
def other_people_can_read_this_chapter(step):
    logout_current_user()
    login_another_user(step)
    i_visit_book_index_page(step)
    find_book_in_list(world.book_id).should_has_class("unread")
    i_read_a_book(step)
    find(".chapters_pagination .chapter-list option[value='%s']" % (world.old_total_chapters + 1)).click()

@step(u'my posted chapter was increased')
def my_posted_chapter_was_increased(step):
    default_user().book_profile.chapters_count.should.equal(world.user_total_chapter_before_post + 1)

@step(u'I edit that chapter')
def i_edit_that_chapter(step):
    find("#edit-chapter").click()
    new_chapter_form = find("#new-chapter-form")
    new_chapter_form.find("input[name='title']").send_keys("Title was edited")
    new_chapter_form.find("textarea[name='content']").fillin("Content was edited")
    new_chapter_form.find("button[type='submit']").click()

@step(u'Then I see that chapter was edited')
def then_i_see_that_chapter_was_edited(step):
    chapter = find("#chapter")
    find(".notifications").text.should.contain("Your chapter was edited successfully.")
    chapter.find("h2").text.should.contain("Title was edited")
    chapter.find(".content").text.should.contain("Content was edited")

@step(u'I see the post new chapter form')
def i_see_the_post_new_chapter_form(step):
    world.chapter_form = find("#new-chapter-form")

@step(u'I fill title for this chapter "([^"]*)"')
def i_fill_title_for_this_chapter(step, title):
    world.chapter_form.find("input[name='title']").send_keys(title)

@step(u'I fill the next chapter number for this chapter')
def i_fill_the_next_chapter_number_for_this_chapter(step):
    world.user_total_chapter_before_post = default_user().book_profile.chapters_count
    world.old_total_chapters = current_book().chapters_count
    world.chapter_form.find("input[name='number']").send_keys(str(current_book().chapters_count + 1))

@step(u'I enter chapter content "([^"]*)"')
def i_enter_chapter_content(step, content):
    world.chapter_form.find("textarea[name='content']").fillin(content)

@step(u'I select language for this chapter')
def i_select_language_for_this_chapter(step):
    world.chapter_form.find("select[name='language']").select("language-0")

@step(u'chapter title is "([^"]*)"')
def chapter_title_is(step, title):
    find("#chapter h2").text.should.contain(title)

@step(u'chapter content is "([^"]*)"')
def chapter_content_is(step, content):
    find("#chapter .content").text.should.contain(content)
