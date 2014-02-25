'''
Created on Dec 8, 2013

@author: antipro
'''

from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField()

    class Meta:
        app_label = 'thankshop'
