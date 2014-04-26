import os

from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.utils.decorators import method_decorator

from book.models import Book
from book.models.attachment_model import Attachment
from decorator.ajax_required_decorator import ajax_required
from limiter.utils import LimitChecker
from tangthuvien import settings
from tangthuvien.django_custom import HttpJson
from django.utils.translation import ugettext as _

class UploadAttachmentView(View):

    @method_decorator(ajax_required)
    @method_decorator(login_required)
    @LimitChecker.check("HOURLY_USER_UPLOAD_LIMIT")
    @LimitChecker.check("HOURLY_IP_UPLOAD_LIMIT")
    def post(self, request):
        returnJson = {}

        book_id = request.REQUEST.get('book_id', 0)
        book = Book.objects.get(pk=book_id)

        upload = request.FILES.get('file')
        if upload:
            destination = os.path.join(book.upload_attachment_dir, upload.name)
            destination_full = settings.media_path(destination)
            with open(destination_full, "w") as des:
                for chunk in upload.chunks():
                    des.write(chunk)
            attachment = Attachment.objects.create(
                            uploader=request.user,
                            book=book,
                            name=upload.name,
                            file=destination,
                            size=os.path.getsize(destination_full),
                            is_approved=request.user.has_perm('book.can_approve_attachment'),
                            downloads_count=0,
                        )
            returnJson['files'] = [{
                'name': attachment.name,
                'url': attachment.download_url,
                'size': attachment.size,
                'creation_date': attachment.creation_date.strftime("%D %d %M %Y")
            }]
        return HttpJson(returnJson)

LimitChecker.register(__name__, "HOURLY_USER_UPLOAD_LIMIT",
                      _("You uploaded %(counter)d of %(limit)d attachments in 1 hour. "
                        "So you can not upload any attachments until next hour. "
                        "Please try again"), 10, timeout_func='timeout_to_next_hour')

LimitChecker.register(__name__, "HOURLY_IP_UPLOAD_LIMIT",
                      _("Your IP uploaded %(counter)d of %(limit)d attachments in 1 hour. "
                        "So you can not upload any attachments until next hour. "
                        "Please try again"), 100, timeout_func='timeout_to_next_hour',
                      key_func='get_user_ip')
