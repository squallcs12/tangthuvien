'''
Created on Jul 29, 2013

@author: antipro
'''
from django.contrib import admin
from django.conf import settings
from custom_admin.filters import TextColumnFilter, ForeignKeyColumnFilter
from django.db.models.fields import Field, FieldDoesNotExist
from django.db.models.fields.related import RelatedField, ManyToOneRel, \
    ForeignKey, OneToOneField

import pdb
import inspect

class ModelAdminColumnFilter(admin.ModelAdmin):
    column_filters = {}
    disabled_column_filters = ()

    def __init__(self, model, admin_site):
        self.current_column_filters = {}
        for key in self.list_display:
            if key in self.column_filters:
                self.current_column_filters[key] = self.column_filters[key](key)
            elif key not in self.disabled_column_filters:
                try:
                    field_type = model._meta.get_field(key)  # @UnusedVariable
                    if isinstance(field_type, Field) and not isinstance(field_type, RelatedField) and not isinstance(field_type, ManyToOneRel):
                        self.current_column_filters[key] = TextColumnFilter(key)
                    elif isinstance(field_type, ForeignKey):
                        if isinstance(field_type, OneToOneField):
                            pass
                        else:
                            self.current_column_filters[key] = ForeignKeyColumnFilter(key, field_type)
                except FieldDoesNotExist:
                    pass

        self.origin_list_filter = self.list_filter
        self.list_filter += tuple(self.current_column_filters.values())
        admin.ModelAdmin.__init__(self, model, admin_site)

    def get_changelist_real(self, *args, **kwargs):
        return super(ModelAdminColumnFilter, self).get_changelist(*args, **kwargs)

    def get_changelist(self, request, **kwargs):
        if self.origin_list_filter:
            return self.get_changelist_real(request, **kwargs)
        return FakechangeList(self, request, **kwargs)

    class Media:
        js = (settings.STATIC_URL + "custom_admin/changelist_view.js",)

class FakechangeList(object):
    def __init__(self, admin, request, **kwargs):
        self.admin = admin
        self.request = request
        self.kwagrs = kwargs

    def __call__(self, *args, **kwargs):
        changelist = self.admin.get_changelist_real(self.request, **self.kwagrs)(*args, **kwargs)
        changelist.has_filters = False
        return changelist
