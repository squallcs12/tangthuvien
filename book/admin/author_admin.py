'''
Created on Jul 27, 2013

@author: antipro
'''
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name', 'slug')

