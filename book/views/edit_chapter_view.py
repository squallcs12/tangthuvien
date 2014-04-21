'''
Created on Sep 21, 2013

@author: antipro
'''
from book.models import Chapter
from book.forms import EditChapterForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _

@login_required
def main(request, chapter_id, edit_chapter_form=EditChapterForm, template="book/edit_chapter.html"):
    data = {}
    chapter = Chapter.objects.get(pk=chapter_id)
    book = chapter.book
    data['chapter'] = chapter

    if request.method == 'POST':
        form = EditChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your chapter was edited successfully."))
            return HttpResponseRedirect(reverse('read_book_chapter', kwargs={'slug':book.slug, 'chapter_number': chapter.number}))
    else:
        form = EditChapterForm(instance=chapter)

    data['form'] = form

    return TemplateResponse(request, template, data)
