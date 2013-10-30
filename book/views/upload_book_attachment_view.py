from tangthuvien.django_custom import HttpJson
from book.models import Book
from tangthuvien import settings

import os

@login_required
def ajax(request, book_id):
	returnJson = {}

	book = Book.objects.get(pk=book_id)

	upload = request.FILES.get('file')
	if upload:
		destination = os.path.join(book.upload_attachment_dir, upload.file_name)
		destination_full = settings.realpath(destination)
		with open(destination_full, "w") as des:
			for chunk in upload.chunks():
				des.write(chunk)
		attachment = Attachment.objects.create(
						uploader=request.user,
						book=book,
						name=upload.file_name,
						url=destination,
						size=os.path.getsize(destination_full),
						is_approved=False,
					)
		returnJson['files'] = [{
			'name': attachment.name,
			'url': attachment.real_url,
			'size': attachment.size,
			'date_creation': attachment.date_creation.strftime("%D %d %M %Y")
		}]
	return HttpJson(returnJson)
