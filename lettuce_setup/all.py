'''
Created on Jul 25, 2013

@author: antipro
'''
from lettuce import after, before, world
from selenium import webdriver

@before.each_scenario
def before_scenario(scenario):
    world.browser = webdriver.Firefox()

@after.each_scenario
def after_scenario(scenario):
    world.browser.quit()
