'''
Created on Jul 30, 2013

@author: antipro
'''
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class UserLog(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey('book.Book')
    page = models.IntegerField()
    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)

    class Meta:
        app_label = 'book'
