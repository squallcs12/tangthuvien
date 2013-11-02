'''
Created on Jul 29, 2013

@author: antipro
'''

import os
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tagging import fields
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from .rating_model import RatingLog

from datetime import timedelta
from tangthuvien import settings
from unidecode import unidecode
from django.template.defaultfilters import slugify
from tangthuvien.rediscache import cache_it

class Book(models.Model):

    STATUS_ONGOING = 0
    STATUS_FINISHED = 1

    user = models.ForeignKey(User)
    tags = fields.TagField(_('tags'))
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to=settings.BOOK_COVER_MEDIA_PATH)
    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        help_text=_("Used to build the book's URL."))
    description = models.TextField(blank=True)
    author = models.ForeignKey('book.Author')
    categories = models.ManyToManyField(
        'book.Category',
        related_name='books',
        blank=True, null=True,
        verbose_name=_('categories'))
    complete_status = models.IntegerField(default=0)
    ttv_type = models.ForeignKey('book.BookType')
    sites = models.ManyToManyField(
        Site,
        related_name='books',
        verbose_name=_('sites'),
        help_text=_('Sites where the entry will be published.'))
    favorite_count = models.IntegerField(default=0)
    favorited_by = models.ManyToManyField(User, related_name="favorite_books", through='book.Favorite')
    read_users = models.ManyToManyField(User, related_name="read_books", through="book.UserLog")
    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)
    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)
    chapters_count = models.IntegerField(default=0)

    _chapters_list = None

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self._chapters_list = None

    def is_rated_by(self, user):
        try:
            RatingLog.objects.get(book=self, user=user)
            return True
        except ObjectDoesNotExist:
            return False

    def is_favorited_by(self, user):
        return self.favorited_by.filter(id=user.id).exists()

    class Meta:
        """
        CoreEntry's meta informations.
        """
        abstract = False
        app_label = 'book'
        ordering = ['-creation_date']
        get_latest_by = 'creation_date'
        verbose_name = _('book')
        verbose_name_plural = _('books')
        permissions = (('can_view_all', 'Can view all books'),
                       ('can_change_status', 'Can change status'),
                       ('can_change_author', 'Can change author(s) 1'),)

    def __unicode__(self):
        return self.title

    @property
    def full_url(self):
        return "%s%s" % (reverse('books_home'), self.slug,)

    @property
    def is_read(self):
        return self.last_update < timezone.now() + timedelta(minutes= -15)

    @property
    def cover_thumb(self):
        return os.path.join(settings.BOOK_COVER_THUMB_DIR, self.cover.name)

    @property
    def prc_file_name(self):
        return "%s.prc" % self.slug

    @property
    def prc_file(self):
        return "books/prc/%s" % self.prc_file_name

    @property
    def html_file(self):
        return "books/prc/%s.html" % self.slug

    @property
    def upload_attachment_dir(self):
        return "books/attachments/%s" % self.id

    @property
    def chapters_list(self):
        if self._chapters_list is None:
            self._chapters_list = get_chapters_list(self.id)
        return self._chapters_list

    def reset_chapters_list(self):
        get_chapters_list.clear(self.id)

    def is_read_by_user(self, user):
        try:
            return self.last_update < self.userlog_set.get(user=user, book=self).last_update
        except ObjectDoesNotExist:
            return False

    def _create_cover_thumbnail(self):
        if not self.cover:
            return

        from PIL import Image  # @UnresolvedImport
        import imghdr

        # Set our max thumbnail size in a tuple (max width, max height)

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(self.cover.path)
        PIL_TYPE = imghdr.what(self.cover.path)

        image.thumbnail(settings.BOOK_COVER_THUMB_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        thumb_file = os.path.join(settings.MEDIA_ROOT, settings.BOOK_COVER_THUMB_DIR, self.cover.name)
        image.save(thumb_file, PIL_TYPE)

    def _create_slug(self):
        self.slug = slugify(unidecode(self.title))

    def save(self, *args, **kwargs):
        # create slug
        self._create_slug()

        ret = super(Book, self).save(*args, **kwargs)

        # create a thumbnail
        self._create_cover_thumbnail()

        return ret

@cache_it(expire=60*60*24*7)
def get_chapters_list(book_id):
    book = Book.objects.get(pk=book_id)
    chapter_list = []
    for chapter in book.chapter_set.all().order_by('number'):
        chapter_list.append([chapter.number, chapter.title])
    return chapter_list
