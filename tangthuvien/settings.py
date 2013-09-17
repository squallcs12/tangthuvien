# Django settings for tangthuvien project.
import os

PATH_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def realpath(path):
    return os.path.realpath(os.path.join(PATH_ROOT, path))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tangthuvien',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'tangthuvien',
        'PASSWORD': 'random_password',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = realpath('media') + '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = realpath('static') + '/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j-a1ok7-buyuumxep6p0r&#66llfahe%k&s5^k9k8%_=)1@3p3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'tangthuvien.context_processors.site_name',
    'tangthuvien.context_processors.style_list',
    'tangthuvien.context_processors.onetime_show_notification',
  )  # Optional

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tangthuvien.middleware.ClearTemplateJsCss',
)

ROOT_URLCONF = 'tangthuvien.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tangthuvien.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    realpath("templates")
)
LETTUCE_APPS = (
    'book',
    'accounts',
)
RELISH_APPS = (
    'book',
)
RELISH_PROJECT_NAME = 'tangthuvien'
RELISH_PROJECT_VERSION = '1.0'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'lettuce.django',
    'tagging',
    'mptt',
    'south',
    'book',
    'django_coverage',
    'ckeditor',
    'custom_admin',
    'accounts',
    'relish',
    'social_auth',
    'tangthuvien',
)
SITE_ID = 1


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/var/log/tangthuvien.vn/django.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'MYAPP': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

CKEDITOR_UPLOAD_PATH = realpath("media/uploads/ckeditor")

# Book configuration
BOOK_LIST_ITEM_COUNT = 10
BOOK_COVER_MEDIA_PATH = 'books/covers'
BOOK_COVER_THUMB_DIR = 'thumbs'
BOOK_COVER_THUMB_SIZE = [210, 280]
BOOK_CHAPTER_PAGINATOR_RANGE = (-100, -50, -10, -2, -1, 0, 1, 2, 10, 50, 100)


# social auth

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)
TWITTER_CONSUMER_KEY = 'VCbibbV9XJ0NN12m7KXUrQ'
TWITTER_CONSUMER_SECRET = 'xZ4aXbHVBMe1Hh7hETRnXAYb01j1DFiBiAVVvcrQc0M'
FACEBOOK_APP_ID = '163282880528447'
FACEBOOK_API_SECRET = '10da9db623ab2ce4a5d9cec50be0ae82'
GOOGLE_OAUTH2_CLIENT_ID = '458888079280.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'ts4n76udRMzz96kwNc5QdaiZ'

SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/accounts/set_password'

SOCIAL_AUTH_UID_LENGTH = 222
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 200
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 135
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 125

FACEBOOK_APP_ACCESS_TOKEN = '163282880528447|IyNyMAZGdb_Wej9QwkWLRdo4N9Q'

# disqus config
DISQUS_DEVELOPER = True
DISQUS_SHORTNAME = 'tangthuvien'

# redis config
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_ONETIME_NOTIFICATION_PREFIX = "ONETIME_NOTIFICATION_"

AVAILABLE_STYLES = ['amelia', 'cerulean', 'cosmo', 'cyborg', 'flatly', 'journal', 'readable', 'simplex', 'slate', 'spacelab', 'united']
DEFAULT_STYLE = 'slate'
REDIS_STYLE_USER_SETTING_KEY = 'STYLE'

REDIS_USER_SETTING_KEY_PREFIX = 'USER_SETTINGS_'

try:
    from local_settings import *
except ImportError:
    pass
