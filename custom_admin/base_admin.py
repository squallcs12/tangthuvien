'''
Created on Jul 29, 2013

@author: antipro
'''
from django.contrib import admin
from django.conf import settings
from custom_admin.filters import TextColumnFilter

class ModelAdminColumnFilter(admin.ModelAdmin):
    column_filters = {}

    def __init__(self, model, admin_site):
        self.current_column_filters = {}
        for key in self.list_display:
            if key in self.column_filters:
                self.current_column_filters[key] = self.column_filters[key](key)
            else:
                self.current_column_filters[key] = TextColumnFilter(key)

        self.list_filter += tuple(self.current_column_filters.values())
        admin.ModelAdmin.__init__(self, model, admin_site)

    class Media:
        js = (settings.STATIC_URL + "custom_admin/changelist_view.js",)
