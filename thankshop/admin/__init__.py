from django.contrib import admin
from thankshop import models
from . import package_admin
from thankshop.admin import item_admin

admin.site.register(models.Package, package_admin.PackageAdmin)
admin.site.register(models.ThankPoint)
admin.site.register(models.Item, item_admin.ItemAdmin)
