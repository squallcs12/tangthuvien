'''
Created on Oct 30, 2013

@author: antipro
'''

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from book.admin.filter_base import RelatedSimpleListFilter
from book.models.book_model import Book


class BookFilter(RelatedSimpleListFilter):
    """
    List filter for EntryAdmin with published authors only.
    """
    model = Book
    lookup_key = 'book_id'
    title = _('Books')
    parameter_name = 'attachment'

    verbose_name = _('attacment')
    verbose_name_plurar = _('attachments')


class AttachmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['book', 'file']}),
    ]

    list_display = ('book', 'name', 'size', 'uploader', 'creation_date')
    list_editable = ()

    list_filter = [BookFilter]

    list_display_links = ('name',)

    actions_on_top = True
    actions_on_bottom = True

    def save_model(self, request, obj, form, change):
        obj.uploader = request.user
        obj.size = obj.file.size
        obj.name = obj.file.name
        obj.is_approved = True
        obj.save()
