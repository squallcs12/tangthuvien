from django.db import models
from django.utils import importlib

class Tracker(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    error_message = models.CharField(max_length=255)
    timeout_module = models.CharField(max_length=255)
    timeout_func = models.CharField(max_length=255)
    limit = models.PositiveIntegerField()

    def get_timeout(self):
        try:
            # import module
            module = importlib.import_module(self.timeout_module)
        except ImportError:  # class importing
            # split module path
            components = self.timeout_module.split(".")

            # class name is the last component
            class_name = components.pop()

            # constructure module name
            module_name = ".".join(components)

            # import
            module = importlib.import_module(module_name)
            module = getattr(module, class_name)

        return getattr(module, self.timeout_func)()

    def check_error_message(self):
        if "%(counter)d" not in self.error_message:
            raise Exception("Missing counter parameter")

        if "%(limit)d" not in self.error_message:
            raise Exception("Missing limit parameter")

    def save(self, *args, **kwargs):
        self.check_error_message()
        super(Tracker, self).save(*args, **kwargs)

from django import dispatch
from django.db.models.signals import post_save

@dispatch.receiver(post_save, sender=Tracker)
def create_book_profile(sender, **kwargs):
    from limiter import utils
    _limiter = kwargs.get('instance')
    utils.LimitChecker.limiters[_limiter.code] = _limiter
