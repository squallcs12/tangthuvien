from django.http.response import HttpResponseNotAllowed
from django.utils.translation import ugettext as _
import json
from django.conf import settings

def thank_points_required(thank_points):
    def thank_points_decorator(func):
        def decorator(request, *args, **kwargs):
            if request.user.thank_point.thank_points + thank_points < 0:
                response = HttpResponseNotAllowed(["not_enough_thank_points"])
                response['messages'] = json.dumps({
                    'error' : [
                        _("You need at least %(number)d thank points to do thank") % {'number' :-thank_points}
                    ]
                });
                return response
            return func(request, *args, **kwargs)
        return decorator
    return thank_points_decorator
