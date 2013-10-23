# -*- coding: utf-8 -*-
'''
Created on Jul 28, 2013

@author: antipro
'''
from book.models import BookType
import factory

class BookTypeFactory(factory.Factory):
    FACTORY_FOR = BookType

    name = factory.Sequence(lambda n: 'book-type-{0}'.format(n))
