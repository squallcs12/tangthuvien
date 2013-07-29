from django.contrib.admin.filters import SimpleListFilter
import pdb

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

    def render(self):
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
    def render(self):
        return '<input type="text" name="%(name)s" id="filter_column_id_%(name)s" class="filter_column" style="width: 95%%" value="%(value)s"/>' \
                % {'name' : self.parameter_name, 'value' : self.value if self.value else ''}

class MatchTextColumnFilter(TextColumnFilter):
    '''
    Text contants filter
    '''
    def queryset(self, request, queryset):
        if self.value is not None:
            params = {'%s__icontains' % self.column_name : self.value}
            return queryset.filter(**params)
