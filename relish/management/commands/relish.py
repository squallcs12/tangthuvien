'''
Created on Aug 9, 2013

@author: antipro
'''
from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option
import os
from django.utils.importlib import import_module
import subprocess
import shutil


def get_apps():
    return map(import_module, settings.INSTALLED_APPS)

def _filter_bultins(module):
    "returns only those apps that are not builtin django.contrib"
    name = module.__name__
    return not name.startswith("django.contrib") and name != 'RELISH.django'


def _filter_configured_apps(module):
    "returns only those apps that are in django.conf.settings.RELISH_APPS"
    app_found = True
    if hasattr(settings, 'RELISH_APPS') and isinstance(settings.RELISH_APPS, tuple):
        app_found = False
        for appname in settings.RELISH_APPS:
            if module.__name__.startswith(appname):
                app_found = True

    return app_found


def _filter_configured_avoids(module):
    "returns apps that are not within django.conf.settings.RELISH_AVOID_APPS"
    run_app = False
    if hasattr(settings, 'RELISH_AVOID_APPS') and isinstance(settings.RELISH_AVOID_APPS, tuple):
        for appname in settings.RELISH_AVOID_APPS:
            if module.__name__.startswith(appname):
                run_app = True

    return not run_app

def is_relish_file(filename):
    file_name, file_extension = os.path.splitext(filename)  # @UnusedVariable
    if file_extension in ('.feature', '.md'):
        return True
    return False


def collect_relish(only_the_apps=None, avoid_apps=None, path="features"):
    """gets all installed apps that are not from django.contrib
    returns a list of tuples with (path_to_app, app_module)
    """

    apps = get_apps()

    if isinstance(only_the_apps, tuple) and any(only_the_apps):

        def _filter_only_specified(module):
            return module.__name__ in only_the_apps
        apps = filter(_filter_only_specified, apps)
    else:
        apps = filter(_filter_bultins, apps)
        apps = filter(_filter_configured_apps, apps)
        apps = filter(_filter_configured_avoids, apps)

    if isinstance(avoid_apps, tuple) and any(avoid_apps):

        def _filter_avoid(module):
            return module.__name__ not in avoid_apps

        apps = filter(_filter_avoid, apps)

    joinpath = lambda app: (os.path.join(os.path.dirname(app.__file__), path), app)
    return map(joinpath, apps)

def _filter_feature_path_exists(path):
    return os.path.exists(path[0])

def tree(path):
    for root, dirs, files in os.walk(path):  # @UnusedVariable
        for filename in files:
            yield os.path.join(root, filename)

class Command(BaseCommand):
    help = """
    Publish cucumber feature files to relishapp.com
    """

    option_list = BaseCommand.option_list + (
        make_option('-a', '--apps', action='store', dest='apps', default='',
             help='Run ONLY the django apps that are listed here. Comma separated'),
        make_option('-A', '--avoid-apps', action='store', dest='avoid_apps', default='',
             help='AVOID running the django apps that are listed here. Comma separated'),
        make_option('-f', '--folder', action='store', dest='folder', default='features',
             help='Features folder name'),
        make_option('-t', '--tmp', action='store', dest='tmp', default='.feature_symlinks',
             help='Features folder name'),
    )

    def path_to_run(self, apps_to_run, apps_to_avoid):
        return (1,)

    def get_paths(self, args, apps_to_run, apps_to_avoid, features_folder):
        return collect_relish(apps_to_run, apps_to_avoid, features_folder)

    def handle(self, *args, **options):
        folder = options.get('tmp', '.feature_symlinks')
        features_folder = options.get('folder', 'features')
        apps_to_run = tuple(options.get('apps', '').split(","))
        apps_to_avoid = tuple(options.get('avoid_apps', '').split(","))
        paths = self.get_paths(args, apps_to_run, apps_to_avoid, features_folder)

        paths = filter(_filter_feature_path_exists, paths)

        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, 0775)
        for path, module in paths:
            os.makedirs(os.path.join(folder, module.__name__), 0775)
            for root, dirs, files in os.walk(path):  # @UnusedVariable
                for filename in files:
                    if is_relish_file(filename):
                        relative_folder = root[len(path):]
                        if relative_folder:
                            if relative_folder[0] == os.sep:
                                relative_folder = relative_folder[1:]
                            des_folder = os.path.join(folder, module.__name__, relative_folder)
                            if not os.path.isdir(des_folder):
                                os.mkdir(des_folder, 0775)
                            os.symlink(os.path.join(root, filename), os.path.join(des_folder , filename))
                        else:
                            os.symlink(os.path.join(root, filename), os.path.join(folder, module.__name__, filename))

        subprocess.call(["relish", "push", '%s:%s' % (settings.RELISH_PROJECT_NAME, settings.RELISH_PROJECT_VERSION), "path", folder])
