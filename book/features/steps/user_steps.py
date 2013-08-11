'''
Created on Aug 3, 2013

@author: antipro
'''
from lettuce import step
from lettuce_setup.function import *  # @UnusedWildImport

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
