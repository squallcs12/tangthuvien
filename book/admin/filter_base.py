'''
Created on Jul 28, 2013

@author: antipro
'''
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import ungettext_lazy
from django.utils.translation import ugettext_lazy as _

class RelatedSimpleListFilter(SimpleListFilter):

    model = None
    lookup_key = None
    title = None
    parameter_name = None
    verbose_name = ''
    verbose_name_plurar = ''

    def queryset(self, request, queryset):
        """
        Return the object's entries if a value is set.
        """
        if self.value():
            params = {self.lookup_key: self.value()}
            return queryset.filter(**params)

    def lookups(self, request, model_admin):
        """
        Return published objects with the number of entries.
        """
        active_objects = self.model.objects.all()
        for active_object in active_objects:
            active_object.number_of_entries = getattr(active_object, '%s_set' % self.parameter_name).count()

        for active_object in active_objects:
            yield (
                str(active_object.pk), ungettext_lazy(
                    '%(item)s (%(count)i %(verbose_name)s)',
                    '%(item)s (%(count)i %(verbose_name_plurar)s)',
                    active_object.number_of_entries) % {
                        'item': active_object.__unicode__(),
                        'count': active_object.number_of_entries,
                        'verbose_name_plurar' : self.verbose_name_plurar,
                        'verbose_name' : self.verbose_name, })
