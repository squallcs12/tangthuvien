'''
Created on Aug 4, 2013

@author: antipro
'''
from django.http.response import HttpResponse
from book.models.chapter_model import Chapter
from book.models.chapter_thank_model import ChapterThank
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from book.signals import chapter_thank_signal
from tangthuvien.decorator.ajax_required_decorator import ajax_required
from django.conf import settings
from thankshop.decorators import thank_points_required, \
    thank_points_interval_required

THANK_RESPONSE_CODE_FAIL = 0
THANK_RESPONSE_CODE_SUCCESS = 1
THANK_RESPONSE_CODE_ALREADY_THANK = 2

@ajax_required
@login_required
@thank_points_required(settings.THANKSHOP_THANK_POINTS_COST)
@thank_points_interval_required
def main(request):
    try:
        chapter_id = int(request.POST.get('chapter_id'))
    except ValueError:
        return HttpResponse(THANK_RESPONSE_CODE_FAIL)

    chapter = Chapter.objects.get(pk=chapter_id)

    try:
        ChapterThank.objects.get(chapter=chapter, user=request.user)
        return HttpResponse(THANK_RESPONSE_CODE_ALREADY_THANK)
    except ObjectDoesNotExist:
        pass

    chapter.thank_count += 1
    chapter.save()

    chapterThank = ChapterThank(chapter=chapter, user=request.user)
    chapterThank.save()

    chapter_thank_signal.send(main, chapter=chapter, user=request.user)

    return HttpResponse(THANK_RESPONSE_CODE_SUCCESS)
