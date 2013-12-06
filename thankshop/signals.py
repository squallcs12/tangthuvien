'''
Created on Dec 4, 2013

@author: eastagile
'''
from django import dispatch
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
import datetime
from django.core.exceptions import ObjectDoesNotExist
from book import signals as book_signals
from django.utils import timezone

def log_user_daily_logged_in(sender, user, request, **kwargs):
    from thankshop import models
    models.UserDailyLoginHistory.log(user)

user_logged_in.connect(log_user_daily_logged_in)

# when user read a chapter
user_first_daily_login = dispatch.Signal(providing_args=["user"])

@dispatch.receiver(user_first_daily_login)
def increaase_thank_points(sender, **kwargs):
    user = kwargs.get('user')
    from thankshop import models
    try:
        today = timezone.now().date()
        previous_login = models.UserDailyLoginHistory.objects.get(user=user, date__lt=today)
        timediff = today - previous_login.date
        if timediff.days > 1:
            notlogin_days = timediff.days - 1
            user.thank_point.increase_thank_points(
                settings.THANKSHOP_DAILY_NOT_LOGIN_THANK_POINTS * notlogin_days,
                models.ThankPoint.DAILY_NOT_LOGIN
            )

    except ObjectDoesNotExist:
        pass

    user.thank_point.increase_thank_points(
        settings.THANKSHOP_DAILY_LOGIN_THANK_POINTS,
        models.ThankPoint.DAILY_LOGIN
    )

@dispatch.receiver(book_signals.chapter_thank_signal)
def user_spend_thank_points(sender, **kwargs):
    user = kwargs.get('user')
    chapter = kwargs.get('chapter')
    from thankshop import models

    thank_obj = user.thank_point
    thank_obj.set_timeout(settings.THANKSHOP_THANK_INTERVAL)
    thank_obj.increase_thank_points(settings.THANKSHOP_THANK_POINTS_COST, models.ThankPoint.THANK_COST)
    chapter.user.thank_point.increase_thanked_points(-settings.THANKSHOP_THANK_POINTS_COST *
                                                     settings.THANKSHOP_THANK_POINTS_PERCENT,
                                                      models.ThankPoint.THANKED)
