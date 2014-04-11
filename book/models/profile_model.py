'''
Created on Sep 20, 2013

@author: antipro
'''
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tangthuvien import settings

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="book_profile")
    # books_count = models.IntegerField(help_text=_('Number of books was posted by this user'))
    chapters_count = models.IntegerField(default=0, help_text=_('Number of chapters was posted by this user'))
    upload_attachments_count = models.IntegerField(default=0, help_text=_('Number of attachments was uploaded by this user'))
    daily_uploaded_attachments_count = models.IntegerField(default=0, help_text=_('Number of attachments was uploaded by this user in current day'))
    daily_approved_attachments_count = models.IntegerField(default=0, help_text=_('Number of attachments was approved by this user in current day'))
    daily_downloaded_attachments_count = models.IntegerField(default=0, help_text=_('Number of attachments was downloaded by this user in current day'))

    @property
    def can_upload_attachment(self):
        return self.daily_uploaded_attachments_count < settings.BOOK_ATTACHMENTS_COUNT_UPLOAD_LIMIT

    @property
    def can_approve_attachment(self):
        return self.daily_approved_attachments_count < settings.BOOK_ATTACHMENTS_COUNT_APPROVE_LIMIT

    @property
    def can_download_attachment(self):
        return self.daily_downloaded_attachments_count < settings.BOOK_ATTACHMENTS_COUNT_DOWNLOAD_LIMIT

    class Meta:
        app_label = 'book'
