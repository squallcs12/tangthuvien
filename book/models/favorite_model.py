'''
Created on Aug 16, 2013

@author: antipro
'''
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Favorite(models.Model):
    book = models.ForeignKey('book.Book')
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)

    class Meta:
        app_label = 'book'
