'''
Created on Oct 18, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from book.forms import PublishNewBookForm
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

@login_required
def main(request, post_new_book_form=PublishNewBookForm, template="book/publish_new_book.phtml"):
    data = {}

    if request.method == "POST":
        form = post_new_book_form(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.process()
            return HttpResponseRedirect(reverse('post_new_chapter', kwargs={'book_id':book.id}))
    else:
        form = post_new_book_form(request)

    data['form'] = form

    return TemplateResponse(request, template, data)
