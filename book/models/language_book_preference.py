'''
Created on Feb 27, 2014

@author: antipro
'''
from django.db import models
from django.contrib.auth.models import User

class LanguagePreference(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey("book.Book")
    language = models.ForeignKey("book.Language")

    class Meta:
        app_label = "book"
        unique_together = (("user", "book"),)
