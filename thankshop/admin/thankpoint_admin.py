'''
Created on Feb 24, 2014

@author: eastagile
'''
from django.contrib import admin

class ThankpointAdmin(admin.ModelAdmin):
    list_display = ('user', 'thank_points', 'thanked_points')

