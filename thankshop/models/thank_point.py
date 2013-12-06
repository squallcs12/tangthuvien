'''
Created on Dec 4, 2013

@author: eastagile
'''
from django.db import models
from django.contrib.auth.models import User
from tangthuvien.models.fields import AutoOneToOneField
from django.utils import datetime_safe

class ThankPoint(models.Model):
    user = AutoOneToOneField(User, related_name="thank_point")
    thank_points = models.IntegerField(default=0)
    thanked_points = models.IntegerField(default=0)
    max_thanked_points = models.IntegerField(default=0)

    DAILY_LOGIN = 'dailylogin'
    DAILY_NOT_LOGIN = 'dailynotlogin'
    THANK_COST = 'thankcost'
    
    THANKED = 'thanked'

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

    class Meta:
        app_label = 'thankshop'

class ThankPointHistory(models.Model):
    user = models.ForeignKey(User)
    points = models.IntegerField()
    datetime = models.DateTimeField(default=datetime_safe.datetime.now)
    key = models.CharField(max_length=255)

    class Meta:
        app_label = 'thankshop'
