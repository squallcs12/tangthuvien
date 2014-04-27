'''
Created on Apr 21, 2014

@author: eastagile
'''
from limiter.exceptions import LimiterException
from django.http.response import HttpResponse
import json

class Limiter(object):
    def process_exception(self, request, exception):
        if isinstance(exception, LimiterException):
            response = HttpResponse(status=400)
            response['messages'] = json.dumps({"error": [exception.message]})
            return response
