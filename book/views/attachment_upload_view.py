from django.contrib.auth.decorators import login_required

from tangthuvien.django_custom import HttpJson
from book.models import Book
from tangthuvien import settings

import os
from book.models.attachment_model import Attachment

@login_required
def ajax(request, book_id):
	returnJson = {}

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
