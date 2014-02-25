'''
Created on Dec 4, 2013

@author: eastagile
'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserDailyLoginHistory(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()

    @classmethod
    def log(cls, user):
        assert isinstance(user, User)
        if not cls.objects.filter(user=user, date=timezone.now().date()).exists():
            login_history = cls(user=user, date=timezone.now().date())
            login_history.save()
            return True
        return False

    class Meta:
        app_label = 'thankshop'
