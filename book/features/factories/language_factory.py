'''
Created on Jul 30, 2013

@author: antipro
'''

import factory
from book.models import Language

class LanguageFactory(factory.Factory):
    FACTORY_FOR = Language

    name = factory.Sequence(lambda n: 'language-{0}'.format(n))
