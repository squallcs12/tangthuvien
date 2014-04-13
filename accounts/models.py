from django.db import models
from django.contrib.auth.models import User
from awesome_avatar.fields import AvatarField

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^awesome_avatar\.fields\.AvatarField"])
except:
    pass

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = AvatarField(upload_to='avatars', width=100, height=100)

    def __unicode__(self):
        return 'Profile for user %s' % self.user_id
