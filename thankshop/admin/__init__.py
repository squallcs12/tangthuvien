from django.contrib import admin
from thankshop import models
from thankshop.admin import thankpoint_admin

admin.site.register(models.Package)
admin.site.register(models.ThankPoint, thankpoint_admin.ThankpointAdmin)
admin.site.register(models.Item)
