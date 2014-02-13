'''
Created on Dec 15, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from thankshop.models.item import Item
from tangthuvien.django_custom import HttpJson

@login_required
def index(request, username="me", template="thankshop/inventory.phtml"):
    data = {}
    return TemplateResponse(request, template, data)

@login_required
def list_items(request, user_id="me"):
    if user_id == "me":
        user = request.user
    else:
        user = User.objects.get(pk=user_id)

    item_ids = user.thankshop_items.values_list("item_id", flat=True)
    items = Item.objects.filter(id__in=item_ids)

    return HttpJson(items)
