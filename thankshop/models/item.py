'''
Created on Dec 14, 2013

@author: antipro
'''
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    long_description = models.TextField()
    price = models.IntegerField()
    stocks = models.IntegerField()
    image = models.ImageField(upload_to='thankshop/item_images/')

    class Meta:
        app_label = 'thankshop'
