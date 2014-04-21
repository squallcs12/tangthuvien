from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

# Create your models here.
class Feedback(models.Model):
    date = models.DateTimeField(default=timezone.now)
    subject = models.CharField(_("Subject"), max_length=255)
    content = models.TextField(_("Content"))
    attachment = models.FileField(_("Attachment"), upload_to='feedback', blank=True)
    url = models.URLField(_("Url"), default='')
    ip = models.IPAddressField(default='0.0.0.0')
