'''
Created on Oct 27, 2013

@author: antipro
'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import os

def upload_to(instance, filename):
    return os.path.join(instance.book.upload_attachment_dir, filename)

class Attachment(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_to, default="")
    size = models.IntegerField()
    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now)
    uploader = models.ForeignKey(User)
    book = models.ForeignKey('book.Book')
    downloads_count = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)


    @property
    def real_url(self):
        return self.file.url  # return url from home

    @property
    def json_output(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.download_url,
            'size': self.size,
            'creation_date': self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        }

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
        permissions = (('can_approve_attachment', 'Can approve uploaded attachment'),)
