'''
Created on Aug 4, 2013

@author: antipro
'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from book.models.book_model import Book
from django.utils.translation import ugettext_lazy as _

class ChapterThank(models.Model):
    chapter = models.ForeignKey('book.Chapter')
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'book'

class ChapterThankSummary(models.Model):
    chapter = models.OneToOneField('book.Chapter', primary_key=True)
    users = models.TextField()

    class Meta:
        app_label = 'book'
