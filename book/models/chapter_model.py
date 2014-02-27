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
from book.models.language_model import Language

class Chapter(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    language = models.ForeignKey('book.Language', null=True)
    content = RichTextField()
    thank_count = models.IntegerField(default=0)

    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)

    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)

    @property
    def languages(self):
        language_ids = Chapter.objects.filter(book=self.book, number=self.number).values_list("language_id", flat=True)
        return Language.objects.filter(id__in=language_ids)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'book'
        unique_together = (("book", "number", "language"),)
