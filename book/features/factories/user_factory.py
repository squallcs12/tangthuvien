'''
Created on Jul 30, 2013

@author: antipro
'''

import factory
from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User
