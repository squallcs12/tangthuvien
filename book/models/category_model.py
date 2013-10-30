'''
Created on Jul 29, 2013

@author: antipro
'''
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from unidecode import unidecode
from django.template.defaultfilters import slugify


class EntryRelatedPublishedManager(models.Manager):
    """Manager to retrieve objects associated with published entries"""

    def get_query_set(self):
        """Return a queryset containing published entries"""
        return super(
            EntryRelatedPublishedManager, self).get_query_set().filter(
                books__sites=Site.objects.get_current()
            ).distinct()


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

    def _create_slug(self):
        self.slug = slugify(unidecode(self.title))

    def save(self, *args, **kwargs):
        self._create_slug()

        return super(Category, self).save(*args, **kwargs)
