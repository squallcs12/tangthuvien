'''
Created on Oct 24, 2013

@author: antipro
'''
from book.forms import AddBookTypeForm
from tangthuvien.django_custom import HttpJson

def ajax(request, new_type_form=AddBookTypeForm):
    returnJson = {}
    form = new_type_form(request.POST, prefix='type')
    returnJson['success'] = False
    if form.is_valid():
        ttv_type = form.process()
        returnJson['success'] = True
        returnJson['id'] = ttv_type.id
        returnJson['name'] = ttv_type.name

    return HttpJson(returnJson)
