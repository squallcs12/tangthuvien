'''
Created on Oct 31, 2013

@author: antipro
'''

from django.db import models

class Copy(models.Model):
    thread_id = models.IntegerField(unique=True)
    book = models.OneToOneField('book.Book')
    last_page = models.IntegerField()
    last_post = models.IntegerField()
    last_chapter_number = models.IntegerField()
    is_done = models.BooleanField()

    class Meta:
        app_label = 'book'
