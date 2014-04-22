'''
Created on Apr 22, 2014

@author: antipro
'''
from django.contrib import admin
from limiter.models import Limiter

# Register your models here.
class LimiterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('id', 'code', 'description', 'error_message',
                    'timeout_module', 'timeout_func', 'limit')}),
    ]
    readonly_fields = ('id', 'code', 'description', 'error_message',
                    'timeout_module', 'timeout_func')
    list_display = ('id', 'code', 'description', 'error_message',
                    'timeout_module', 'timeout_func', 'limit')

    search_fields = ('code', 'error_message', 'timeout_module', 'timeout_func')

    list_editable = ('limit',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Limiter, LimiterAdmin)
