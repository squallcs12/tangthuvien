'''
Created on Sep 14, 2013

@author: antipro
'''
from . import settings as st
import redis

pool = redis.ConnectionPool(host=st.REDIS_HOST, port=st.REDIS_PORT, db=st.REDIS_DB)
redis_cli = redis.Redis(connection_pool=pool)


class UserSettings(object):
    @classmethod
    def wrap(cls, key):
        return '%s%s' % (st.REDIS_USER_SETTING_KEY_PREFIX, key)

    @classmethod
    def get(cls, key, user_id):
        return redis_cli.hget(cls.wrap(key), user_id)

    @classmethod
    def set(cls, key, user_id, value):
        redis_cli.hset(cls.wrap(key), user_id, value)
