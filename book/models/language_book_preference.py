'''
Created on Feb 27, 2014

@author: antipro
'''
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from tangthuvien.functions import UserSettings
from django.conf import settings

class LanguagePreference(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey("book.Book")
    language = models.ForeignKey("book.Language")

    @classmethod
    def get_preference(cls, book, user):
        try:
            language_preference = cls.objects.get(book=book, user=user)
            return language_preference.language_id
        except ObjectDoesNotExist:
            language_preference_global = UserSettings.get(settings.BOOK_LANGUAGE_PREFER_KEY, user.id)
            if language_preference_global:
                return language_preference_global[0]

        return None

    class Meta:
        app_label = "book"
        unique_together = (("user", "book"),)
