from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
from ckeditor.fields import RichTextField

from .book_model import Book
from .category_model import Category
from .chapter_model import Chapter
from .user_log_model import UserLog
from .chapter_thank_model import ChapterThank, ChapterThankSummary
from .rating_model import Rating, RatingLog
from .favorite_model import Favorite
from .profile_model import Profile
from .attachment_model import Attachment
from .copy_model import Copy

class BookType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def _create_slug(self):
        self.slug = slugify(unidecode(self.name))

    def save(self, *args, **kwargs):
        # create slug
        self._create_slug()

        return super(BookType, self).save(*args, **kwargs)

    class Meta:
        app_label = 'book'

class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255,
        help_text=_("Used to build the author's URL."))
    information = RichTextField(blank=True)

    def __unicode__(self):
        return self.name

    def _create_slug(self):
        self.slug = slugify(unidecode(self.name))

    def save(self, *args, **kwargs):
        # create slug
        self._create_slug()

        return super(Author, self).save(*args, **kwargs)

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

