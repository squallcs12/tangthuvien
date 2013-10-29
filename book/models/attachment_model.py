'''
Created on Oct 27, 2013

@author: antipro
'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class Attachment(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    size = models.IntegerField()
    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)
    uploader = models.ForeignKey(User)
    book = models.ForeignKey('book.Book')
    downloads_count = models.IntegerField()
    is_approved = models.BooleanField()
    
    
    @property
    def real_url(self):
        if self.url.startswith("/") or (self.url.find("//") != -1): # if a valid url
            return self.url
        return "/%s" % self.url #return url from home
    @property
    def download_url(self):
        return reverse(
                    'book_attachment_download',
                    kwargs={
                        'book_id': self.book.id,
                        'attachment_id': self.id
                    })
    
    class Meta:
        """
        CoreEntry's meta informations.
        """
        abstract = False
        app_label = 'book'
        ordering = ['-creation_date']
        get_latest_by = 'creation_date'
        verbose_name = _('attachment')
        verbose_name_plural = _('attachment')
        permissions = (('can_approve', 'Can approve uploaded attachment'),)