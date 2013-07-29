from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

from zinnia.models.entry import TagsEntry
from zinnia.models.category import Category
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

class EntryRelatedPublishedManager(models.Manager):
    """Manager to retrieve objects associated with published entries"""

    def get_query_set(self):
        """Return a queryset containing published entries"""
        return super(
            EntryRelatedPublishedManager, self).get_query_set().filter(
                books__sites=Site.objects.get_current()
            ).distinct()

# Create your models here.

class Category(MPTTModel):
    """
    Simple model for categorizing entries.
    """

    title = models.CharField(
        _('title'), max_length=255)

    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        help_text=_("Used to build the category's URL."))

    description = models.TextField(
        _('description'), blank=True)

    parent = TreeForeignKey(
        'self',
        related_name='children',
        null=True, blank=True,
        verbose_name=_('parent category'))

    objects = TreeManager()
    published = EntryRelatedPublishedManager()

    def books_published(self):
        """
        Returns category's published entries.
        """
        return self.books

    @property
    def tree_path(self):
        """
        Returns category's tree path
        by concatening the slug of his ancestors.
        """
        if self.parent_id:
            return '/'.join(
                [ancestor.slug for ancestor in self.get_ancestors()] +
                [self.slug])
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        """
        Builds and returns the category's URL
        based on his tree path.
        """
        return ('zinnia_category_detail', (self.tree_path,))

    def __unicode__(self):
        return self.title

    class Meta:
        """
        Category's meta informations.
        """
        app_label = 'book'
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        """
        Category MPTT's meta informations.
        """
        order_insertion_by = ['title']


class Book(TagsEntry):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        help_text=_("Used to build the book's URL."))
    description = models.TextField(blank=True)
    author = models.ForeignKey('book.Author')
    categories = models.ManyToManyField(
        Category,
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

class BookType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    information = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Chapter(models.Model):
    book = models.ForeignKey('book.Book')
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

    class Meta(Book.Meta):
        pass

class ChapterType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

