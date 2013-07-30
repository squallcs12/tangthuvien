'''
Created on Jul 30, 2013

@author: antipro
'''
from django.db import models
from django.contrib.auth.models import User

class UserLog(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey('book.Book')
    page = models.IntegerField()

    class Meta:
        app_label = 'book'
