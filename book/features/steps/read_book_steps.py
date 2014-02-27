# -*- coding: utf-8 -*-
'''
Created on Jul 29, 2013

@author: antipro
'''
from lettuce_setup.function import *  # @UnusedWildImport
import random
from book.models.book_model import Book
from book.models.chapter_model import Chapter
from book.models import Language
from book.features.factories.book_factory import BookFactory
from book.features.factories.chapter_factory import ChapterFactory
from book.features.steps.general import *
from book.models.language_book_preference import LanguagePreference
from tangthuvien.functions import UserSettings

@step(u'I click on a book')
def i_click_on_a_book(step):
    book_div = find_all("#books .book").pop()
    world.book_id = book_div.get_attribute('item_id')
    world.book = Book.objects.get(pk=world.book_id)
    book_div.find("a.title").click()

@step(u'I see the book title and description')
def i_see_the_book_title_and_description(step):
    find("#book .panel-heading").text.should_not.be.empty
    find("#book .panel-body").text.should_not.be.empty

@step(u'I see the author name and information')
def i_see_the_author_name_and_information(step):
    find("#author .panel-heading").text.should_not.be.empty
    find("#author .panel-body").text.should_not.be.empty

def check_chapter(number):
    find("#chapter .number").text.should.equal(str(number))
    find("#chapter .content").text.should_not.be.empty

@step(u'I see the first chapter')
def i_see_the_first_chapter(step):
    check_chapter(1)

@step(u'I go to next chapter')
def i_go_to_next_chapter(step):
    find(".chapters_pagination").find_all(".pagination a").pop().click()

@step(u'see the second chapter')
def see_the_second_chapter(step):
    check_chapter(2)

def go_to_chapter(number):
    find(".chapters_pagination .chapter-list option[value='%s']" % number).click()

@step(u'I choose a random chapter from selection box')
def i_choose_a_random_chapter_from_selection_box(step):
    world.random_chapter_choose = random.randint(2, 5)
    go_to_chapter(world.random_chapter_choose)

@step(u'see a random chapter')
def see_a_random_chapter(step):
    check_chapter(world.random_chapter_choose)

@step(u'I click on the previous book')
def i_click_on_the_previous_book(step):
    find("#books .book[item_id='%s'] a.title" % world.book_id).click()

@step(u'see the last random chapter')
def see_the_last_random_chapter(step):
    see_a_random_chapter(step)

@step(u'I go to last chapter')
def i_go_to_last_chapter(step):
    find_all(".chapters_pagination .chapter-list option").pop().click()

@step(u'see the last chapter')
def see_the_last_chapter(step):
    find_all(".chapters_pagination .pagination a").pop().should_be_temp_link()

@step(u'a book exists in "([^"]*)" languages')
def a_book_exists_in_group1_languages(step, count):
    book = BookFactory()
    book.save()
    for language in Language.objects.all()[0: int(count)]:
        book.languages.add(language)
    book.save()
    world.book_id = book.id

@step(u'that book contain chapters:')
def that_book_contain_chapters(step):
    for chapter_data in step.hashes:
        chapter = ChapterFactory()
        chapter.book_id = world.book_id
        chapter.number = int(chapter_data['number'])
        chapter.title = chapter_data['title']
        chapter.language = Language.objects.get(name=chapter_data['language'])
        chapter.save()

@step(u'I visit this book introduction page')
def i_visit_this_book_introduction_page(step):
    read_book_by_id(world.book_id)


@step(u'I see a languages prefer contain "([^"]*)"')
def i_see_a_languages_prefer_contain(step, languages):
    prefer_languages = [elm.text for elm in find_all("#languages .language")]
    prefer_languages.should.equal(languages.split(","))

@step(u'I choose "([^"]*)" as prefer language')
def i_choose_group1_as_prefer_language(step, language):
    for language_button in find_all("#languages .language"):
        if language_button.text == language:
            language_button.click()

@step(u'I go to chapter "([^"]*)"')
def i_go_to_chapter(step, chapter_number):
    go_to_chapter(int(chapter_number))

@step(u'I see a list of languages contain "([^"]*)"')
def i_see_a_list_of_languages_contain(step, languages):
    find("#change_chapter_language button").click()
    i_see_a_languages_prefer_contain(step, languages)
    find("#change_chapter_language button").click()

@step(u'I choose language "([^"]*)"')
def i_choose_language(step, language):
    find("#change_chapter_language button").click()
    i_click_on(step, language)

@step(u'"([^"]*)" is the selected language of this book')
def language_is_the_selected_language_of_this_book(step, language):
    book = Book.objects.get(pk=world.book_id)
    preference = LanguagePreference.objects.get(book=book, user=default_user())
    preference.language.name.should.equal(language)

@step(u'I setting my language prefer to "([^"]*)"')
def i_setting_my_language_prefer_to(step, languages):
    languages = languages.split(",")
    settings_dict = []
    for language in languages:
        settings_dict.append(Language.objects.get(name=language).id)
    UserSettings.set(settings.BOOK_LANGUAGE_PREFER_KEY, default_user().id, settings_dict)
