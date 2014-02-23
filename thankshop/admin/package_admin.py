'''
Created on Feb 23, 2014

@author: antipro
'''
from django.contrib import admin

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'points')
