'''
Created on Aug 8, 2013

@author: antipro
'''
from book.models.book_model import Book
from django.http.response import Http404
from django.views.generic.base import View

from tangthuvien.decorator.ajax_required_decorator import ajax_required
from tangthuvien.django_custom import HttpJson
from django.utils.decorators import method_decorator
from limiter.utils import LimitChecker
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

class RatingView(View):

    @method_decorator(ajax_required)
    @method_decorator(login_required)
    @LimitChecker.check("DAILY_USER_RATING_LIMIT")
    @LimitChecker.check("DAILY_IP_RATING_LIMIT")
    def post(self, request):
        number = int(request.POST.get('number'))
        book_id = int(request.POST.get('book_id'))

        book = Book.objects.get(pk=book_id)
        if number not in range(1, 6):
            raise Http404()

        book.rating.add_rating(request.user, number)

        returnJson = {}
        returnJson['average_result'] = book.rating.average_result
        returnJson['rating_count'] = book.rating.rating_count

        return HttpJson(returnJson)


LimitChecker.register(__name__, "DAILY_USER_RATING_LIMIT",
                      _("You has use %(counter)d of %(limit)d rating today. "
                        "Thus you can not rating until tomorrow."), 200)

LimitChecker.register(__name__, "DAILY_IP_RATING_LIMIT",
                      _("You has use %(counter)d of %(limit)d rating today. "
                        "Thus you can not rating until tomorrow."), 2000,
                      key_func='get_user_ip')
