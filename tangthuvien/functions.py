'''
Created on Sep 14, 2013

@author: antipro
'''
from . import settings as st
import redis

def disqus_append(data):
    data.update(
        DISQUS_SHORTNAME=st.DISQUS_SHORTNAME,
        DISQUS_DEVELOPER=st.DISQUS_DEVELOPER
    )

pool = redis.ConnectionPool(host=st.REDIS_HOST, port=st.REDIS_PORT, db=st.REDIS_DB)
redis_cli = redis.Redis(connection_pool=pool)

def wrap(key):
    return '%s%s' % (st.REDIS_USER_SETTING_KEY_PREFIX, key)

def get_user_settings(key, user_id):
    return redis_cli.hget(wrap(key), user_id)

def change_user_settings(key, user_id, value):
    redis_cli.hset(wrap(key), user_id, value)
