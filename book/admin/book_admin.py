'''
Created on Jul 27, 2013

@author: antipro
'''
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from book.models import Chapter, Author, Language
from book.admin.filter_base import RelatedSimpleListFilter
from custom_admin.filters import TextColumnFilter, MatchTextColumnFilter
from custom_admin.base_admin import ModelAdminColumnFilter

class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0

class BookAdmin(ModelAdminColumnFilter):
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'cover', 'author', 'description', 'categories', 'complete_status', 'languages']}),
    ]

#     inlines = [ChapterInline]

    list_display = ('id', 'title', 'slug', 'cover', 'cover_thumb', 'author', 'get_categories', 'complete_status')
    list_display_links = ('id', 'title', 'slug', 'complete_status',)

    column_filters = {
        'id' : TextColumnFilter,
        'title' : MatchTextColumnFilter,
    }

    list_filter = ['languages', 'author']

    def get_categories(self, entry):
        """Return the categories linked in HTML"""
        try:
            categories = ['<a href="%s" target="blank">%s</a>' %
                          (category.get_absolute_url(), category.title)
                          for category in entry.categories.all()]
        except NoReverseMatch:
            categories = [category.title for category in
                          entry.categories.all()]
        return ', '.join(categories)
    get_categories.allow_tags = True
    get_categories.short_description = _('category(s)')

    actions_on_top = True
    actions_on_bottom = True

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'user'):
            obj.user = request.user
        obj.save()
