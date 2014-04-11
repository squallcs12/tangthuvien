'''
Created on Dec 4, 2013

@author: eastagile
'''
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.utils.translation import ugettext as _

class ThankPoint(models.Model):
    user = models.OneToOneField(User, related_name="thank_point")
    thank_points = models.IntegerField(default=0)
    thanked_points = models.IntegerField(default=0)
    max_thanked_points = models.IntegerField(default=0)
    timeout = models.DateTimeField(default=timezone.now)

    DAILY_LOGIN = 'dailylogin'
    DAILY_NOT_LOGIN = 'dailynotlogin'
    THANK_COST = 'thankcost'

    THANKED = 'thanked'

    def set_timeout(self, seconds):
        timeout = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        self.timeout = timezone.make_aware(timeout, timezone.utc)

    def timeout_remain(self):
        now = timezone.make_aware(datetime.datetime.utcnow(), timezone.utc)
        if self.timeout > now:
            timediff = self.timeout - now
            return timediff.seconds
        return 0

    def increase_thank_points(self, points, key):
        self.thank_points += points
        self.save()
        self.log(points, key)

    def increase_thanked_points(self, points, key):
        self.thanked_points += points
        self.save()
        self.log(points, key)

    def log(self, points, key):
        ThankPointHistory(
            user=self.user,
            points=points,
            key=key,
        ).save()

    def __unicode__(self):
        return _("User ID %s thank point") % self.user_id

    class Meta:
        app_label = 'thankshop'

class ThankPointHistory(models.Model):
    user = models.ForeignKey(User)
    points = models.IntegerField()
    datetime = models.DateTimeField(default=timezone.now)
    key = models.CharField(max_length=255)

    class Meta:
        app_label = 'thankshop'
