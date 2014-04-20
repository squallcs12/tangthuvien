from django.db import models
from django.utils import timezone

# Create your models here.
class Feedback(models.Model):
    date = models.DateTimeField(default=timezone.now)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    attachment = models.FileField(upload_to='feedback')
    url = models.URLField(default='')
    ip = models.IPAddressField(default='0.0.0.0')
