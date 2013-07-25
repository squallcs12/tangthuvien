'''
Created on Jul 25, 2013

@author: antipro
'''
from lettuce_setup import all
from lettuce import world
from lettuce.django import django_url
import pdb

def browser():
    '''
    @return: selenium.webdriver.Firefox
    '''
    return world.browser

def visit(url):
    browser().get(django_url(url))
    
def find_all(selector):
    return browser().find_elements_by_css_selector(selector)

def find(selector):
    return browser().find_element_by_css_selector(selector)

def previous_page_link(selector):
    return find(selector + " .pagination .prev")

def next_page_link(selector):
    return find(selector + " .pagination .next")

def last_page_link(selector):
    return find(selector + " .pagination .last")