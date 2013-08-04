'''
Created on Jul 30, 2013

@author: antipro
'''
from django import dispatch
import pdb
from book.models.user_log_model import UserLog
from django.core.exceptions import ObjectDoesNotExist

# when user read a chapter
chapter_read_signal = dispatch.Signal(providing_args=["user", "chapter", "page"])

# when user thank a chapter
chapter_thank_signal = dispatch.Signal(providing_args=["user", "chapter"])

# require login to do something
def require_login_simple(func):
    def decorator(*args, **kwargs):
        user = kwargs.get('user')
        if not user or not user.is_authenticated():
            return
        func(*args, **kwargs)
    return decorator

@dispatch.receiver(chapter_read_signal)
@require_login_simple
def log_user_read_book(sender, **kwargs):
    user = kwargs.get('user')
    if not user.id:
        return
    page = kwargs.get('page')
    chapter = kwargs.get('chapter')
    book = chapter.book

    try:
        userLog = UserLog.objects.get(user=user, book=book)
        userLog.page = page
    except ObjectDoesNotExist:
        userLog = UserLog(user=user, book=book, page=page)

    userLog.save()

@dispatch.receiver(chapter_read_signal)
@require_login_simple
def set_thanked_status(sender, **kwargs):
    user = kwargs.get('user')
    chapter = kwargs.get('chapter')

    from book.models import ChapterThank
    try:
        chapterThank = ChapterThank.objects.get(user=user, chapter=chapter)  # @UnusedVariable
        chapter.thanked_by_current_user = True
    except ObjectDoesNotExist:
        chapter.thanked_by_current_user = False

