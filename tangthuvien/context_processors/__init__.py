from django.contrib.sites.models import Site
from tangthuvien.context_processors.OnetimeShowNotification_processor import OnetimeShowNotification

def site_name(request):
    return {'SITE_NAME': Site.objects.get_current().name}

def onetime_show_notification(request):
    return {'onetime_show_notification' : OnetimeShowNotification(request)}


