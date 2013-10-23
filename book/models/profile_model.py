'''
Created on Sep 20, 2013

@author: antipro
'''
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tangthuvien.models.fields import AutoOneToOneField

class Profile(models.Model):
    user = AutoOneToOneField(User, related_name="book_profile")
    # books_count = models.IntegerField(help_text=_('Number of books was posted by this user'))
    chapters_count = models.IntegerField(default=0, help_text=_('Number of chapters was posted by this user'))

    class Meta:
        app_label = 'book'
