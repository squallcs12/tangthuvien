'''
Created on Oct 29, 2013

@author: antipro
'''
from book.models.attachment_model import Attachment
from django.contrib.auth.decorators import login_required
from tangthuvien.django_custom import HttpJson
from django.utils.translation import ugettext_lazy as _

@login_required
def ajax(request):
    returnJson = {}

    attachment_id = request.GET.get('attachment_id')
    book_profile = request.user.book_profile

    if book_profile.can_approve_attachment:
        attachment = Attachment.objects.get(pk=attachment_id)
        attachment.is_approved = True
        attachment.save()

        book_profile.daily_approved_attachments_count += 1
        book_profile.save()

        returnJson['status'] = 'success'
    else:
        returnJson['status'] = 'fail'
        returnJson['message'] = _("You reach the limited of book attachments approving count")

    return HttpJson(returnJson)
