'''
Created on Jul 25, 2013

@author: antipro
'''
from lettuce import after, world

@after.each_scenario
def after_scenario(scenario):
    if hasattr(world, 'browser'):
        world.browser.quit()
        del world.browser
