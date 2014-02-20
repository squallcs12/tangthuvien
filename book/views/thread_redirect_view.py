'''
Created on Feb 20, 2014

@author: eastagile
'''
from book.models.copy_model import Copy
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.translation import ugettext as _

def main(request, thread_id=0):
    try:
        copy = Copy.objects.get(thread_id=thread_id)
        return HttpResponseRedirect(reverse('book_read', kwargs={'slug': copy.book.slug}))
    except ObjectDoesNotExist:
        messages.error(request, _("This book was not copied to this site."))
        return HttpResponseRedirect("%s?tid=%s" % (reverse('copy_book'), thread_id))
