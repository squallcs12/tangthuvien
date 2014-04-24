'''
Created on Apr 22, 2014

@author: antipro
'''
import hashlib
import datetime
from django.shortcuts import get_object_or_404
from limiter.exceptions import LimiterException
from tangthuvien.functions import redis_cli
from limiter import models
from django.utils.translation import ugettext as _

get_object_or_404

class LimitChecker(object):

    cli = redis_cli()

    limiters = dict((x.code, x) for x in models.Tracker.objects.all())

    @classmethod
    def refresh_limiters(cls):
        cls.limiters = dict((x.code, x) for x in models.Tracker.objects.all())

    @classmethod
    def register(cls, code, error_message, timeout_module, timeout_func, limit):
        if code in cls.limiters:
            return
        models.Tracker.objects.create(code=code,
                                      error_message=error_message,
                                      timeout_module=timeout_module,
                                      timeout_func=timeout_func,
                                      limit=limit)

    @classmethod
    def md5_key(cls, key):
        return hashlib.sha224(key).hexdigest()

    @classmethod
    def timeout_to_next_day(cls):
        now_time = datetime.datetime.now().time()
        pass_sec = now_time.hour * 3600 + now_time.minute * 60 + now_time.second
        return 24 * 3600 - pass_sec

    @classmethod
    def timeout_to_next_week(cls):
        now = datetime.datetime.now()
        now_time = now.time()
        pass_sec = now_time.hour * 3600 + now_time.minute * 60 + now_time.second
        time_to_next_day = 24 * 3600 - pass_sec
        return time_to_next_day + 24 * 2600 * (6 - now.weekday())

    @classmethod
    def timeout_to_next_hour(cls):
        now_time = datetime.datetime.now().time()
        return 3600 - (now_time.minute * 60 + now_time.second)

    @classmethod
    def check(cls, code, request, raise_error=True):
        key_exists = cls.cli.exists(code)

        # get key
        key = cls.limiters[code].get_key(request)
        if key == None:
            return True

        # current limit counter
        counter = int(cls.cli.hget(code, key))
        limit = cls.limiters[code].limit
        if limit > 0 and counter >= limit:
            if raise_error:
                raise LimiterException(_(cls.limiters[code].error_message)
                                             % {
                                                'counter': counter,
                                                'limit': limit,
                                                })
            return False

        # increase counter
        cls.cli.hincrby(code, key, 1)

        # auto remove this hash
        if not key_exists:
            cls.cli.expire(code, cls.limiters[code].get_timeout())
        return True

    @classmethod
    def weekly(cls, code, request, raise_error=True):
        return cls.check(code,
                  request,
                  raise_error=raise_error)

    @classmethod
    def daily(cls, code, request, raise_error=True):
        return cls.check(code,
                  request,
                  raise_error=raise_error)
    @classmethod
    def hourly(cls, code, request, raise_error=True):
        return cls.check(code,
                  request,
                  raise_error=raise_error)
