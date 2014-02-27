'''
Created on Feb 27, 2014

@author: antipro
'''
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'book'
