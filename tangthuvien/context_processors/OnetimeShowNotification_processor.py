'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien import settings
from tangthuvien.functions import redis_cli
class OnetimeShowNotification(object):

    request = None

    def __init__(self, request):
        self.request = request

    def __getattribute__(self, name):
        if name == 'request':
            return super(OnetimeShowNotification, self).__getattribute__(name)

        if not self.request.user.is_authenticated():
            return False

        name = wrap_key(name)

        return redis_cli.sismember(name, self.request.user.id)

def wrap_key(key):
    return "%s%s" % (settings.REDIS_ONETIME_NOTIFICATION_PREFIX, key)

def register_off(key, user_id):
    redis_cli.sadd(wrap_key(key), user_id)
