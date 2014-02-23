'''
Created on Feb 23, 2014

@author: antipro
'''
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stocks', 'image_html')
    search_fields = ['name']
    list_filter = ['price']
