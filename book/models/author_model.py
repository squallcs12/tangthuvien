'''
Created on Feb 27, 2014

@author: antipro
'''
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode

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

