'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien import settings
from tangthuvien.functions import redis_cli
class OnetimeShowNotification(object):
    request = None
    onetime_notification_keys = []

    def __init__(self, request):
        self.request = request

    def __getattribute__(self, key):
        if key == 'request':
            return super(OnetimeShowNotification, self).__getattribute__(key)

        if not self.request.user.is_authenticated():
            return False

        if key not in OnetimeShowNotification.onetime_notification_keys:
            OnetimeShowNotification.onetime_notification_keys.append(key)

        return is_on(key, self.request.user.id)

def wrap_key(key):
    return "%s%s" % (settings.REDIS_ONETIME_NOTIFICATION_PREFIX, key)

def register_off(key, user_id):
    if key in OnetimeShowNotification.onetime_notification_keys:
        redis_cli.sadd(wrap_key(key), user_id)

def is_on(key, user_id):
    key = wrap_key(key)
    return redis_cli.sismember(key, user_id)
