# -*- coding: utf-8 -*-
'''
Created on Jul 28, 2013

@author: antipro
'''
from book.models import BookType
import factory


def get_type_name(n):
    return ['Dịch', 'Convert', 'Việt'][n]

class BookTypeFactory(factory.Factory):
    FACTORY_FOR = BookType

    name = factory.Sequence(lambda n : get_type_name(n))
