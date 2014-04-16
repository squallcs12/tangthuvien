from django.db import models
from django.contrib.auth.models import User
from awesome_avatar.fields import AvatarField

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^awesome_avatar\.fields\.AvatarField"])
except:
    pass

GENDER_CHOICES = (
                  (True, 'Male'),
                  (False, 'Female'),
                  )

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    fullname = models.CharField(max_length=255, blank=True, default='')
    avatar = AvatarField(upload_to='avatars', width=200, height=200)
    homepage = models.URLField(default='', blank=True)
    gender = models.BooleanField(default=True, choices=GENDER_CHOICES)
    birthday = models.DateField(blank=True)

    def __unicode__(self):
        return 'Profile for user %s' % self.user_id
