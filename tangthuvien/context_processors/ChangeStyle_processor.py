'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien.functions import redis_cli
from tangthuvien import settings

def current_style(user):
    if not user.is_authenticated():
        return settings.DEFAULT_STYLE
    style = get_user_settings(settings.REDIS_STYLE_USER_SETTING_KEY, user.id)
    if not style:
        style = settings.DEFAULT_STYLE
    return style

def set_style(user, style):

    if user.is_authenticated():
        change_user_settings(settings.REDIS_STYLE_USER_SETTING_KEY, user.id, style)

def wrap(key):
    return '%s%s' % (settings.REDIS_USER_SETTING_KEY_PREFIX, key)

def get_user_settings(key, user_id):
    return redis_cli.hget(wrap(key), user_id)

def change_user_settings(key, user_id, value):
    redis_cli.hset(wrap(key), user_id, value)
