'''
Created on Feb 24, 2014

@author: eastagile
'''
from django.contrib import admin

class ThankpointHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'datetime', 'key')
    list_filter = ['key']
    search_fields = ['key', 'user__username', 'user__first_name', 'user__last_name']

