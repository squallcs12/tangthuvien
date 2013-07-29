'''
Created on Jul 29, 2013

@author: antipro
'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from book.models.book_model import Book
from django.utils.translation import ugettext_lazy as _

class Chapter(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    chapter_type = models.ForeignKey('book.ChapterType')
    content = RichTextField()
    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)

    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)


    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'book'
