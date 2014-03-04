'''
Created on Mar 4, 2014

@author: eastagile
'''
from django.contrib import admin

class UserItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item')
    search_fields = ['item__name', 'user__username']
