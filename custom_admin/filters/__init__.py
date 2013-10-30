from django.contrib.admin.filters import SimpleListFilter
import pdb
from django.template.response import TemplateResponse
from django.template import Context, Template
from django.template.loader import render_to_string

class ColumnFilter(SimpleListFilter):

    template = 'custom_admin/empty.phtml'
    title = 1
    parameter_name = 1

    def choices(self, cl):
        return []

    def get_param_name(self, param_name):
        return 'cl_%s' % param_name

    def __init__(self, param_name):
        self.column_name = param_name
        self.parameter_name = self.get_param_name(param_name)
        self.value = None

    def render(self, context):
        '''
        Render output for column filder
        '''
        raise NotImplemented

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        if self.value is not None:
            params = {self.column_name : self.value}
            return queryset.filter(**params)

    def __call__(self, *args, **kwargs):
        if len(args) == 4:
            for count, thing in enumerate(args):
                if count == 1:
                    lookup_params = thing
                    break
            self.value = None
            if self.parameter_name in lookup_params:
                self.value = lookup_params.pop(self.parameter_name)
        return self

class TextColumnFilter(ColumnFilter):
    '''
    Text compare filter
    '''
    def render(self, context):
        data = {}
        data['name'] = self.parameter_name

        data['value'] = self.value if self.value else ''

        return render_to_string('custom_admin/text_field.phtml', data, context)

class MatchTextColumnFilter(TextColumnFilter):
    '''
    Text contants filter
    '''
    def queryset(self, request, queryset):
        if self.value is not None:
            params = {'%s__icontains' % self.column_name : self.value}
            return queryset.filter(**params)

class ForeignKeyColumnFilter(ColumnFilter):

    def __init__(self, param_name, foreign_key):
        super(ForeignKeyColumnFilter, self).__init__(param_name)
        self.foreign_key = foreign_key

    def get_options(self):
        '''
        Return foreign values
        '''
        for obj in self.foreign_key.rel.to.objects.all():
            yield {'value' : obj.id, 'label' : obj.__unicode__()}

    def render(self, context):
        data = {}
        data['name'] = self.parameter_name

        data['options'] = self.get_options()

        return render_to_string('custom_admin/foreign_key.phtml', data, context)
