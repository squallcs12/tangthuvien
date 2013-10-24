'''
Created on Oct 24, 2013

@author: antipro
'''
from book.forms import AddAuthorForm
from tangthuvien.django_custom import HttpJson

def ajax(request, new_author_form=AddAuthorForm):
    returnJson = {}
    form = AddAuthorForm(request.POST, prefix='author')
    returnJson['success'] = False
    if form.is_valid():
        author = form.process()
        returnJson['success'] = True
        returnJson['id'] = author.id
        returnJson['name'] = author.name

    return HttpJson(returnJson)
