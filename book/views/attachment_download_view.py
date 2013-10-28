'''
Created on Oct 29, 2013

@author: antipro
'''
from book.models.attachment_model import Attachment
from django.http.response import HttpResponseRedirect
def main(request, book_id=0, attachment_id=0):
    attachment = Attachment.objects.get(pk=attachment_id, book_id=book_id)
    
    book_profile = request.user.book_profile
    book_profile.daily_downloaded_attachments_count += 1
    book_profile.save()
    
    attachment.downloads_count += 1
    attachment.save()
    
    return HttpResponseRedirect(attachment.real_url)