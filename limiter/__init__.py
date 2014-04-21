import redis
import hashlib
import datetime
from django.shortcuts import get_object_or_404
from limiter.exceptions import LimiterException

get_object_or_404

class Limiter(object):

    cli = redis.Redis()
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
    def check(cls, group, key, limit, timeout=100, increase=1, raise_error=True):
        key_exists = cls.cli.exists(group)

        # current limit counter
        counter = int(cls.cli.hget(group, key))
        if counter >= limit:
            if raise_error:
                raise LimiterException()
            return False

        # increase counter
        cls.cli.hincrby(group, key, increase)

        # auto remove this hash
        if not key_exists:
            cls.cli.expire(group, timeout)
        return True

    @classmethod
    def weekly(cls, group, key, limit, increase=1, raise_error=True):
        return cls.check(group,
                  key,
                  limit,
                  timeout=cls.timeout_to_next_week(),
                  increase=increase,
                  raise_error=raise_error)

    @classmethod
    def daily(cls, group, key, limit, increase=1, raise_error=True):
        return cls.check(group,
                  key,
                  limit,
                  timeout=cls.timeout_to_next_day(),
                  increase=increase,
                  raise_error=raise_error)
    @classmethod
    def hourly(cls, group, key, limit, increase=1, raise_error=True):
        return cls.check(group,
                  key,
                  limit,
                  timeout=cls.timeout_to_next_hour(),
                  increase=increase,
                  raise_error=raise_error)
