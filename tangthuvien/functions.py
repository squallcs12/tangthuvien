'''
Created on Sep 14, 2013

@author: antipro
'''
from . import settings as st
import redis
import json

def redis_cli():
    if not hasattr(redis_cli, '_redis'):
        pool = redis.ConnectionPool(host=st.REDIS_HOST, port=st.REDIS_PORT, db=st.REDIS_DB)
        redis_cli._redis = redis.Redis(connection_pool=pool)
    return redis_cli._redis

class UserSettings(object):
    @classmethod
    def wrap(cls, key):
        return '%s%s' % (st.REDIS_USER_SETTING_KEY_PREFIX, key)

    @classmethod
    def get(cls, key, user_id):
        settings = redis_cli().hget(cls.wrap(key), user_id)
        if settings is None:
            return None
        return json.loads(settings)

    @classmethod
    def set(cls, key, user_id, value):
        redis_cli().hset(cls.wrap(key), user_id, json.dumps(value))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR', '0.0.0.0')
