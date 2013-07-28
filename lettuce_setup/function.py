'''
Created on Jul 25, 2013

@author: antipro
'''
from lettuce_setup import all
from lettuce import world
from lettuce.django import django_url
import pdb
import sure
from django.utils.translation import ugettext_lazy as _

def browser():
    return world.browser

def visit(url):
    browser().get(django_url(url))

def find_all(selector):
    return browser().find_elements_by_css_selector(selector)

def find(selector):
    return browser().find_element_by_css_selector(selector)

def current_page_link(selector):
    return find(selector + " .pagination .current")

def first_page_link(selector):
    return find(selector + " .pagination .first")

def previous_page_link(selector):
    return find(selector + " .pagination .prev")

def next_page_link(selector):
    return find(selector + " .pagination .next")

def last_page_link(selector):
    return find(selector + " .pagination .last")

def init_list_item_ids(selector):
    if not hasattr(world, 'list_items'):
        world.list_items = {}
    if world.list_items.get(selector) is None:
        world.list_items[selector] = {}

def save_list_item_ids(page, selector):
    init_list_item_ids(selector)
    items = []
    for item_object in find_all(selector):
        items.append(item_object.get_attribute('item_id'));
    world.list_items[selector][page] = items

def compare_list_item_ids(page1, page2, selector):
    init_list_item_ids(selector)
    if page1 not in world.list_items[selector].keys():
        raise Exception("Item list page %s was not saved" % page1)

    if page2 not in world.list_items[selector].keys():
        raise Exception("Item list page %s was not saved" % page2)
    return len(set(world.list_items[selector][page1]) ^ set(world.list_items[selector][page1])).should.equal(0)

def check_title(title):
    find("#content")
    browser().title.should.contain(_(title).__unicode__())
