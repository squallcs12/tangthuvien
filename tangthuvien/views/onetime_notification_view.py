'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien.django_custom import HttpJson
from django.contrib.auth.decorators import login_required
from tangthuvien.context_processors import OnetimeShowNotification_processor

@login_required
def submit(request):
    key = request.POST.get('key')
    OnetimeShowNotification_processor.register_off(key, request.user.id)

    data = {}
    data['status'] = 1
    return HttpJson(data)
