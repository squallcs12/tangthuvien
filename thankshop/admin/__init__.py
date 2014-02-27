from django.contrib import admin
from thankshop import models
from thankshop.admin import item_admin, package_admin, thankpoint_admin, thankpointhistory_admin

admin.site.register(models.Package, package_admin.PackageAdmin)
admin.site.register(models.ThankPoint, thankpoint_admin.ThankpointAdmin)
admin.site.register(models.ThankPointHistory, thankpointhistory_admin.ThankpointHistoryAdmin)
admin.site.register(models.Item, item_admin.ItemAdmin)
