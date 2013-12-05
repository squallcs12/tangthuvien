'''
Created on Dec 4, 2013

@author: eastagile
'''
from lettuce_setup.function import *
from thankshop import models
from django.conf import settings
import time

def check_thank_point(points, user_number = 1):
    commit()
    thank_obj = models.ThankPoint.objects.get(user=default_user())
    thank_obj.thank_points.should.equal(points)

@step(u'I log into the website for the first time in a day')
def i_log_into_the_website_for_the_first_time_in_a_day(step):
    for row in models.UserDailyLoginHistory.objects.all():
        row.delete()
    given_i_was_a_logged_in_user(step)

@step(u'I receive a number of thank points')
def i_receive_a_number_of_thank_points(step):
    check_thank_point(settings.THANKSHOP_DAILY_LOGIN_THANK_POINTS)

@step(u'I re-login again')
def i_re_login_again(step):
    logout_current_user()
    given_i_was_a_logged_in_user(step)

@step(u'I do not receive any thank points')
def i_do_not_receive_any_thank_points(step):
    check_thank_point(settings.THANKSHOP_DAILY_LOGIN_THANK_POINTS)

@step(u'When I do not log into website in the next day')
def i_do_not_log_into_website_in_the_next_day(step):
    logout_current_user()
    login_hostory = models.UserDailyLoginHistory.objects.get(user=default_user)
    login_hostory.date -= datetime.timedelta(days=2)
    login_hostory.save()

@step(u'Then I see my thank points was decreased')
def i_see_my_thank_points_was_decreased(step):
    given_i_was_a_logged_in_user(step)
    check_thank_point(
        settings.THANKSHOP_DAILY_LOGIN_THANK_POINTS * 2
        + settings.THANKSHOP_DAILY_NOT_LOGIN_THANK_POINTS
    )

@step(u'When I thank a poster for a chapter')
def i_thank_a_poster_for_a_chapter(step):
    assert False, 'This step must be implemented'
@step(u'And poster thanked points was increased by those points')
def and_poster_thanked_points_was_increased_by_those_points(step):
    assert False, 'This step must be implemented'
@step(u'When I use all my thank points')
def i_use_all_my_thank_points(step):
    assert False, 'This step must be implemented'
@step(u'Then I can not thank anylonger')
def i_can_not_thank_anylonger(step):
    assert False, 'This step must be implemented'
@step(u'Then I can not give any thank in a short time')
def i_can_not_give_any_thank_in_a_short_time(step):
    assert False, 'This step must be implemented'
@step(u'Given I has thanked points')
def given_i_has_thanked_points(step):
    assert False, 'This step must be implemented'
@step(u'Then I can not receive more than a limited number of thank points for a chapter on a day')
def i_can_not_receive_more_than_a_limited_number_of_thank_points_for_a_chapter_on_a_day(step):
    assert False, 'This step must be implemented'
@step(u'When I go to the buy thank points page')
def i_go_to_the_buy_thank_points_page(step):
    assert False, 'This step must be implemented'
@step(u'Then I see a list of thank points packages')
def i_see_a_list_of_thank_points_packages(step):
    assert False, 'This step must be implemented'
@step(u'When I buy a packages')
def i_buy_a_packages(step):
    assert False, 'This step must be implemented'
@step(u'Then I receive an amount of thank points to spend')
def i_receive_an_amount_of_thank_points_to_spend(step):
    assert False, 'This step must be implemented'
