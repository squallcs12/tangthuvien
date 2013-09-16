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

