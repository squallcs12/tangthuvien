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
    def seconds_to_next_day(cls):
        now_time = datetime.datetime.now().time()
        return 24 * 3600 - now_time.hour * 3600 - now_time.minute * 60 - now_time.second

    @classmethod
    def check(cls, group, key, limit, seconds=100, increase=1):

        key_exists = cls.cli.exists(group)

        # current limit counter
        counter = int(cls.cli.hget(group, key))
        if counter >= limit:
            raise LimiterException()

        # increase counter
        cls.cli.hincrby(group, key, increase)

        # auto remove this hash
        if not key_exists:
            cls.cli.expire(group, seconds)
        return True

    @classmethod
    def daily(cls, group, key, limit, increase=1, raise_error=True):
        cls.check(group,
                  key,
                  limit,
                  seconds=cls.seconds_to_next_day(),
                  increase=increase,
                  raise_error=raise_error)


