from django.contrib.sites.models import Site
from tangthuvien.context_processors.OneTimeShowNotification_processor import OneTimeShowNotification

def site_name(request):
    return {'SITE_NAME': Site.objects.get_current().name}

def one_time_show_notification(request):
    return {'one_time_show_notification' : OneTimeShowNotification(request)}


