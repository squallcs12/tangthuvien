'''
Created on Oct 18, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from book.forms import PublishNewBookForm, AddAuthorForm, AddBookTypeForm
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

@login_required
def main(request, post_new_book_form=PublishNewBookForm, template="book/publish_new_book.phtml"):
    data = {}

    if request.method == "POST":
        form = post_new_book_form(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save()

            messages.success(request, _("New book was published successfully."))
            return HttpResponseRedirect(reverse('post_new_chapter', kwargs={'book_id':book.id}))
    else:
        form = post_new_book_form(request.user)

        author_form = AddAuthorForm(prefix='author')
        type_form = AddBookTypeForm(prefix='type')

        data['author_form'] = author_form
        data['type_form'] = type_form

    data['form'] = form

    return TemplateResponse(request, template, data)
