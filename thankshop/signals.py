'''
Created on Dec 4, 2013

@author: eastagile
'''
from django import dispatch
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from book import signals as book_signals
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from thankshop.models.thank_point import ThankPoint

user_first_daily_login = dispatch.Signal(providing_args=["user", "request"])

def log_user_daily_logged_in(sender, user, request, **kwargs):
    from thankshop import models
    first_daily_login = models.UserDailyLoginHistory.log(user)
    if first_daily_login:
        user_first_daily_login.send(sender, user=user, request=request)

user_logged_in.connect(log_user_daily_logged_in)

# when user read a chapter

@dispatch.receiver(user_first_daily_login)
def increase_thank_points(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get("request")
    from thankshop import models
    if not hasattr(user, 'thank_point'):
        user.thank_point = models.ThankPoint.objects.get(user=user)
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
            messages.success(request, "thankshop/daily_thankpoints_increase.html", extra_tags="template")

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
@dispatch.receiver(post_save, sender=User)
def create_thank_obj(sender, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        thank_obj = ThankPoint(user=user)
        thank_obj.save()
