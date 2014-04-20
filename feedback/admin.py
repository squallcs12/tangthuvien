from django.contrib import admin
from feedback.models import Feedback

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'content', 'url', 'ip', 'date')

    search_fields = ('subject', 'content', 'url', 'ip')

    list_filter = ('date',)

admin.site.register(Feedback, FeedbackAdmin)
