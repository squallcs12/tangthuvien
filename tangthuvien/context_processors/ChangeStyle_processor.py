'''
Created on Sep 17, 2013

@author: antipro
'''
from tangthuvien import settings, functions

def current_style(user):
    if not user.is_authenticated():
        return settings.DEFAULT_STYLE
    style = functions.get_user_settings(settings.REDIS_STYLE_USER_SETTING_KEY, user.id)
    if not style:
        style = settings.DEFAULT_STYLE
    return style

def set_style(user, style):
    if not style in settings.AVAILABLE_STYLES:
        raise InvalidStyleException("Style are not available")

    if user.is_authenticated():
        functions.change_user_settings(settings.REDIS_STYLE_USER_SETTING_KEY, user.id, style)


class InvalidStyleException(Exception):
    pass
