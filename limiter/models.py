from django.db import models
from django.utils import importlib

class Limiter(models.Model):
    code = models.CharField(max_length=255)
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

from django import dispatch
from django.db.models.signals import post_save

@dispatch.receiver(post_save, sender=Limiter)
def create_book_profile(sender, **kwargs):
    from limiter import utils
    _limiter = kwargs.get('instance')
    utils.Limiter.limiters[_limiter.code] = _limiter
