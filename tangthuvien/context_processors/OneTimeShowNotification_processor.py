'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien import settings
from tangthuvien.functions import redis_cli
class OneTimeShowNotification(object):

    request = None

    def __init__(self, request):
        self.request = request

    def __getattribute__(self, name):
        if name == 'request':
            return super(OneTimeShowNotification, self).__getattribute__(name)

        if not self.request.user.is_authenticated():
            return False

        name = "%s%s" % (settings.REDIS_ONE_TIME_NOTIFICATION_PREFIX, name)

        return redis_cli.sismember(name, self.request.user.id)
