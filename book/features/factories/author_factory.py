'''
Created on Jul 28, 2013

@author: antipro
'''
from book.models import Author
import factory


class AuthorFactory(factory.Factory):
    FACTORY_FOR = Author

    name = factory.Sequence(lambda n: 'Author {0}'.format(n))
