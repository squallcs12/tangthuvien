'''
Created on Jul 28, 2013

@author: antipro
'''

from django.contrib import admin
from django.core import urlresolvers
from book.models import ChapterType

from django.db.models import Count
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

class ChapterTypeFilter(SimpleListFilter):
    """
    List filter for EntryAdmin with published authors only.
    """
    model = ChapterType
    lookup_key = 'chapter_type_id'
    title = _('Chapter types')
    parameter_name = 'chapter_type'

    def lookups(self, request, model_admin):
        """
        Return published objects with the number of entries.
        """
        active_objects = self.model.objects.all().annotate(
            number_of_entries=Count('id'))
        for active_object in active_objects:
            yield (
                str(active_object.pk), ungettext_lazy(
                    '%(item)s (%(count)i chapter)',
                    '%(item)s (%(count)i chapters)',
                    active_object.number_of_entries) % {
                        'item': active_object.__unicode__(),
                        'count': active_object.number_of_entries})

    def queryset(self, request, queryset):
        """
        Return the object's entries if a value is set.
        """
        if self.value():
            params = {self.lookup_key: self.value()}
            return queryset.filter(**params)

class BookTitleFilter(object):

    def has_output(self):
        return True

class ChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['book', 'number', 'title', 'chapter_type', 'content']}),
    ]

    list_display = ('get_book', 'title', 'number', 'chapter_type')

    list_filter = [ChapterTypeFilter, ]

    list_display_links = ('title', 'number')

    actions_on_top = True
    actions_on_bottom = True


    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'user'):
            obj.user = request.user
        obj.save()

    def get_book(self, chapter):
        edit_url = urlresolvers.reverse('admin:book_book_change', args=(chapter.book.id,))
        return '<a href="%s">%s</a>' % (edit_url, chapter.book.__unicode__())
    get_book.allow_tags = True
