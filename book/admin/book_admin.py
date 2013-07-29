'''
Created on Jul 27, 2013

@author: antipro
'''
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.db.models import Count
from django.utils.translation import ungettext_lazy
from django.utils.translation import ugettext_lazy as _
from zinnia.admin.filters import RelatedPublishedFilter
from book.models import Category, Chapter, Author, BookType
from django.contrib.markup.templatetags.markup import markdown
from book.admin.filter_base import RelatedSimpleListFilter
from custom_admin.filters import TextColumnFilter, MatchTextColumnFilter
from custom_admin.base_admin import ModelAdminColumnFilter

class CategoryListFilter(RelatedPublishedFilter):
    """
    List filter for EntryAdmin about categories
    with published entries.
    """
    model = Category
    lookup_key = 'categories__id'
    title = _('published categories')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        """
        Return published objects with the number of entries.
        """
        active_objects = self.model.published.all().annotate(
            number_of_entries=Count('books'))
        for active_object in active_objects:
            yield (
                str(active_object.pk), ungettext_lazy(
                    '%(item)s (%(count)i entry)',
                    '%(item)s (%(count)i entries)',
                    active_object.number_of_entries) % {
                        'item': active_object.__unicode__(),
                        'count': active_object.number_of_entries})

class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0


class AuthorFilter(RelatedSimpleListFilter):
    """
    List filter for EntryAdmin with published authors only.
    """
    model = Author
    lookup_key = 'author_id'
    title = _('Authors')
    parameter_name = 'author'
    verbose_name = _('book')
    verbose_name_plurar = _('books')


class BookTypeFilter(RelatedSimpleListFilter):
    """
    List filter for EntryAdmin with published authors only.
    """
    model = BookType
    lookup_key = 'ttv_type_id'
    title = _('Book types')
    parameter_name = 'ttv_type'

    verbose_name = _('book')
    verbose_name_plurar = _('books')

class BookAdmin(ModelAdminColumnFilter):
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'author', 'description', 'categories', 'complete_status', 'ttv_type']}),
    ]

    inlines = [ChapterInline]

    list_display = ('id', 'title', 'slug', 'author', 'get_categories', 'complete_status', 'ttv_type',)
    list_display_links = ('id', 'title', 'slug', 'complete_status',)

    column_filters = {
        'id' : TextColumnFilter,
        'title' : MatchTextColumnFilter,
    }



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

    def get_markedown_activity_title(self, book):
        return markdown(book.title)
    get_markedown_activity_title.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'user'):
            obj.user = request.user
        obj.save()


