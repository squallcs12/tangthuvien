from django.contrib.sites.models import Site
from tangthuvien.context_processors.OnetimeShowNotification_processor import OnetimeShowNotification
from tangthuvien import settings
from tangthuvien.context_processors.ChangeStyle_processor import current_style
from tangthuvien import settings as st

def site_name(request):
    return {'SITE_NAME': Site.objects.get_current().name}

def style_list(request):
    return {
        'AVAILABLE_STYLES': settings.AVAILABLE_STYLES,
        'CURRENT_STYLE': current_style(request.user),
    }

def socket_io(request):
    return {'SOCKET_IO_URL': settings.SOCKET_IO_URL}

def onetime_show_notification(request):
    return {'onetime_show_notification' : OnetimeShowNotification(request)}
