'''
Created on Apr 22, 2014

@author: antipro
'''
import datetime
from django.shortcuts import get_object_or_404
from limiter.exceptions import LimiterException
from tangthuvien.functions import redis_cli, get_client_ip
from limiter import models
from django.utils.translation import ugettext as _

get_object_or_404

class LimitChecker(object):

    cli = redis_cli()

    limiters = dict((x.code, x) for x in models.Tracker.objects.all())

    @classmethod
    def register(cls, module_name, code, error_message, limit, **kwargs):
        if code in cls.limiters:
            return
        package = module_name.split(".")[0]
        models.Tracker.objects.create(code=code, package=package,
                                      error_message=error_message,
                                      limit=limit, **kwargs)

    @classmethod
    def update(cls, code, **kwargs):
        cls.limiters[code].__dict__.update(**kwargs)
        cls.limiters[code].save()

    @classmethod
    def get_user_id(cls, request):
        if request.user.is_authenticated():
            return request.user.id

    @classmethod
    def get_user_ip(cls, request):
        return get_client_ip(request)

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
    def get_counter(cls, code, request):
        key = cls.get_key(code, request)
        if key == None:
            return None

        counter = cls.cli.hget(code, key)
        if counter:
            return int(counter)
        return 0

    @classmethod
    def get_key(cls, code, request):
        return cls.limiters[code].get_key(request)

    @classmethod
    def _check(cls, code, request, raise_error=True):
        key_exists = cls.cli.exists(code)

        # get key
        key = cls.limiters[code].get_key(request)
        if key == None:
            return True

        # current limit counter
        counter = cls.cli.hget(code, key)
        if counter:
            counter = int(counter)
        else:
            counter = 0

        limit = cls.limiters[code].limit
        if limit > 0 and counter >= limit:
            if raise_error:
                raise LimiterException(_(cls.limiters[code].error_message)
                                             % {
                                                'counter': counter,
                                                'limit': limit,
                                                })
            return False

        # auto remove this hash
        if not key_exists:
            cls.cli.expire(code, cls.limiters[code].get_timeout())
        return True

    @classmethod
    def check(cls, code, raise_error=True):
        def decorator(func):
            def wrapper(self, request, *args, **kwargs):
                cls._check(code, request, raise_error=raise_error)

                response = func(self, request, *args, **kwargs)

                # increase counter
                if response.status < 400: # not error
                    cls.cli.hincrby(code, cls.get_key(code, request), 1)

                return response
            return wrapper
        return decorator

    @classmethod
    def check_func(cls, code, raise_error=True):
        def decorator(func):
            def wrapper(request, *args, **kwargs):
                cls._check(code, request, raise_error=raise_error)

                response = func(request, *args, **kwargs)
                            # increase counter
                if response.status < 400:  # not error
                    cls.cli.hincrby(code, cls.get_key(code, request), 1)

                return response
            return wrapper
        return decorator
