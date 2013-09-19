'''
Created on Jul 25, 2013

@author: antipro
'''
from lettuce_setup import all
from lettuce import world, step, before, after
import pdb
import sure
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from django.db import connection
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import time
from django.db.transaction import TransactionManagementError
from django.conf import settings
import urlparse

def django_url(url="", host='localhost', port=8000):
    base_url = "http://%s" % host
    port = int(port or getattr(settings, 'LETTUCE_SERVER_PORT', 8000))
    if port is not 80:
        base_url += ':%d' % port

    return urlparse.urljoin(base_url, url)

class TimeoutException(Exception):
    pass

def until(method, timeout, message='', ignored_exceptions=True, interval=0.5):
    """Calls the method provided with the driver as an argument until the \
    return value is not False."""
    end_time = time.time() + timeout
    while(True):
        try:
            value = method()
            if value:
                return value
        except ignored_exceptions:
            pass
        time.sleep(0.5)
        if(time.time() > end_time):
            break
    raise TimeoutException(message)

def browser():
    '''
    @return: selenium.webdriver.Firefox
    '''
    if not hasattr(world, 'browser'):
        world.browser = webdriver.Firefox()
        world.browser.implicitly_wait(3)
    return world.browser

def visit(url):
    browser().get(django_url(url))

def visit_by_view_name(name, **kwargs):
    visit(reverse(name, **kwargs))

def find_all(selector):
    return browser().find_elements_by_css_selector(selector)

def find(selector):
    return browser().find_element_by_css_selector(selector)

WebElement.find = WebElement.find_element_by_css_selector
WebElement.find_all = WebElement.find_elements_by_css_selector

def has_class(self, class_name):
    self.get_attribute('class').split(' ').should.contain(class_name);
WebElement.has_class = has_class

def should_be_temp_link(self):
    self.tag_name.should.equal('a')
    self.get_attribute('href').should.equal(browser().current_url + '#')
WebElement.should_be_temp_link = should_be_temp_link

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
    browser().title.should.contain(title)

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

def eval_sql(sql):
    try:
        connection.commit()
    except TransactionManagementError:
        pass
    cursor = connection.cursor()
    cursor.execute(sql)
    value = cursor.fetchone()
    cursor.close()
    return value[0]

@step(u'When I reload the page')
def when_i_reload_the_page(step):
    browser().refresh()


@step(u'Given I was a non-logged-in user')
def given_i_was_a_non_logged_in_user(step):
    pass  # we dont need to do anything for now

@step(u'Given I was a logged-in user')
def given_i_was_a_logged_in_user(step):
    visit_by_view_name('login')
    user = default_user()
    find("#id_username").send_keys(user.username)
    find("#id_password").send_keys(user.raw_password)
    find("#id_login").click()

def random_password():
    return settings.TEST_PASSWORD

def email_address():
    return settings.TEST_EMAIL

@before.all
def clear_redis():
    from tangthuvien.functions import redis_cli
    redis_cli.flushdb()
