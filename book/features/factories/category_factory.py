'''
Created on Oct 21, 2013

@author: antipro
'''
from book.models import Category
import factory

class CategoryFactory(factory.Factory):
    FACTORY_FOR = Category

    title = factory.Sequence(lambda n: 'category-{0}'.format(n))
