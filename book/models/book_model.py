'''
Created on Jul 29, 2013

@author: antipro
'''
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import TagsEntry
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from book.models.rating_model import RatingLog

class Book(TagsEntry):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
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
    complete_status = models.IntegerField()
    ttv_type = models.ForeignKey('book.BookType')

    sites = models.ManyToManyField(
        Site,
        related_name='books',
        verbose_name=_('sites'),
        help_text=_('Sites where the entry will be published.'))

    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)

    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)

    def is_rated_by(self, user):
        try:
            RatingLog.objects.get(book=self, user=user)
            return True
        except ObjectDoesNotExist:
            return False

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
                       ('can_change_author', 'Can change author(s)'),)

    def __unicode__(self):
        return self.title

    @property
    def full_url(self):
        return "%s%s" % (reverse('books_home'), self.slug,)
