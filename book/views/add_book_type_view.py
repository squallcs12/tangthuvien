'''
Created on Oct 24, 2013

@author: antipro
'''
from book.forms import AddLanguageForm
from tangthuvien.django_custom import HttpJson

def ajax(request, new_type_form=AddLanguageForm):
    returnJson = {}
    form = new_type_form(request.POST, prefix='language')
    returnJson['success'] = False
    if form.is_valid():
        ttv_type = form.save()
        returnJson['success'] = True
        returnJson['id'] = ttv_type.id
        returnJson['name'] = ttv_type.name

    return HttpJson(returnJson)
