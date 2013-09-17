from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

from book.models.book_model import Book
from book.models.category_model import Category
from book.models.chapter_model import Chapter
from book.models.user_log_model import UserLog
from book.models.chapter_thank_model import ChapterThank, ChapterThankSummary
from book.models.rating_model import Rating, RatingLog
from book.models.favorite_model import Favorite

class BookType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'book'

class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255,
        help_text=_("Used to build the author's URL."))
    information = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'book'

class Type(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'book'

class ChapterType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'book'

def import_signals():
    from book import signals
import_signals()
