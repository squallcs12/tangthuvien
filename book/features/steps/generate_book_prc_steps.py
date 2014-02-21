'''
Created on Oct 26, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
from book.models.book_model import Book
from book.features.steps.favorite_book_steps import a_new_chapter_was_posted_to_the_book
from book.features.steps.upload_book_attachments_steps import read_book_by_id, get_attachments_list
from django.core.management import call_command
import os
from tangthuvien import settings as st

@step(u'a book exist')
def a_book_exist(step):
    world.book = Book.objects.all()[0]

@step(u'some chapter was posted')
def some_chapter_was_posted(step):
    a_new_chapter_was_posted_to_the_book(step, world.book)

@step(u'after period of time')
def after_period_of_time(step):
    call_command("generate_prc", book=world.book.id)

@step(u'a prc file was generated for this book')
def a_prc_file_was_generated_for_this_book(step):
    prc_file = st.media_path(world.book.prc_file)
    os.path.isfile(prc_file).should.be.true

@step(u'the prc file was listed in the list of attachments')
def the_prc_file_was_listed_in_the_list_of_attachments(step):
    read_book_by_id(world.book.id)
    get_attachments_list().should.contain(world.book.prc_file_name)

@step(u'I press generate prc button')
def i_press_generate_prc_button(step):
    until(lambda : not  find("#generate_book_prc").has_class('disabled'))
    find("#generate_book_prc").click();

@step(u'I see the generate prc process was shown')
def i_see_the_generate_prc_process_was_shown(step):
    find("#generate_book_prc_div .progress").is_displayed().should.be.true

@step(u'the process is done')
def the_process_is_done(step):
    until(lambda: not find("#generate_book_prc_div .progress").is_displayed(), 30)
