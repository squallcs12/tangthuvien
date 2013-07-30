'''
Created on Jul 30, 2013

@author: antipro
'''
from django import dispatch
import pdb
from book.models.user_log_model import UserLog
from django.core.exceptions import ObjectDoesNotExist

# when user read a chapter
chapter_read_signal = dispatch.Signal(providing_args=["user", "book", "page"])




@dispatch.receiver(chapter_read_signal)
def log_user_read_book(sender, **kwargs):
    user = kwargs.get('user')
    if not user.id:
        return
    page = kwargs.get('page')
    book = kwargs.get('book')

    try:
        userLog = UserLog.objects.get(user=user, book=book)
        userLog.page = page
    except ObjectDoesNotExist:
        userLog = UserLog(user=user, book=book, page=page)

    userLog.save()
