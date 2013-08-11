'''
Created on Jul 25, 2013

@author: antipro
'''
from lettuce_setup import all
from lettuce import world, step
from lettuce.django import django_url
import pdb
import sure
from django.utils.translation import ugettext_lazy as _
from selenium.webdriver.remote.webelement import WebElement
from django.db import connection
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

def browser():
    '''
    @return: selenium.webdriver.Firefox
    '''
    return world.browser

def visit(url):
    browser().get(django_url(url))

def visit_by_view_name(name):
    visit(reverse(name))

def find_all(selector):
    return browser().find_elements_by_css_selector(selector)

def find(selector):
    return browser().find_element_by_css_selector(selector)

WebElement.find = WebElement.find_element_by_css_selector
WebElement.find_all = WebElement.find_elements_by_css_selector

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

def execute_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()


def default_user():
    if not hasattr(world, 'default_user'):
        try:
            user = User.objects.create_user('username', 'email@domain.com', 'password')
        except:
            user = User.objects.get_by_natural_key('username')
        user.raw_password = 'password'
        world.default_user = user
    return world.default_user


@step(u'When I reload the page')
def when_i_reload_the_page(step):
    browser().refresh()
