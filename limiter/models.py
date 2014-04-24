from django.db import models
from django.utils import importlib
from tangthuvien.functions import get_client_ip

class Tracker(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    error_message = models.CharField(max_length=255)
    timeout_module = models.CharField(max_length=255)
    timeout_func = models.CharField(max_length=255)
    key_module = models.CharField(max_length=255, default='limiter.models.Tracker')
    key_func = models.CharField(max_length=255, default='get_user_id')
    limit = models.PositiveIntegerField()

    @classmethod
    def get_user_id(cls, request):
        if request.user.is_authenticated():
            return request.user.id

    def get_user_ip(self, request):
        return get_client_ip(request)

    def run(self, module_class, method, *args, **kwargs):
        try:
            # import module
            module = importlib.import_module(module_class)
        except ImportError:  # class importing
            # split module path
            components = module_class.split(".")

            # class name is the last component
            class_name = components.pop()

            # constructure module name
            module_name = ".".join(components)

            # import
            module = importlib.import_module(module_name)
            module = getattr(module, class_name)

        return getattr(module, method)(*args, **kwargs)


    def get_timeout(self):
        return self.run(self.timeout_module, self.timeout_func)

    def get_key(self, request):
        return self.run(self.key_module, self.key_func, request)

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
def update_limiter_list(sender, **kwargs):
    from limiter import utils
    _limiter = kwargs.get('instance')
    utils.LimitChecker.limiters[_limiter.code] = _limiter
