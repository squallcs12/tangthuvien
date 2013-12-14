'''
Created on Dec 14, 2013

@author: antipro
'''
from thankshop import models
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.translation import ugettext as _
import json

@login_required
def ajax(request):
    item_id = int(request.REQUEST['item_id'])
    try:
        item = models.Item.sell(request.user, item_id)

        response = HttpResponse()
        response['messages'] = json.dumps({
                                'success': [_("Item %(name)s was added to your inventory.") % {'name': item.name}]})
    except Exception, e:
        response = HttpResponse()
        response['messages'] = json.dumps({'error': [e.message]})

    return response

