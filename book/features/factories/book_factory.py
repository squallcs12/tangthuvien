'''
Created on Jul 28, 2013

@author: antipro
'''
from book.models import Book, Author, BookType
import factory
from book.features.factories.author_factory import AuthorFactory
import random
from django.contrib.auth.models import User

def get_random_type(n):
    return BookType.objects.all()[n % 3]

def get_ttv_type(n):
    try:
        return get_random_type(n)
    except IndexError:
        for i in range(0, 3):  # @UnusedVariable
            BookType().save()
        return get_random_type(n)


def create_or_get_author():
    try:
        return Author.objects.all()[0]
    except IndexError:
        author = AuthorFactory()
        author.save()
        return author

class BookFactory(factory.Factory):
    FACTORY_FOR = Book

    title = factory.Sequence(lambda n: 'Book Title {0}'.format(n))
    slug = factory.Sequence(lambda n: 'book-title-{0}'.format(n))
    author = factory.Sequence(lambda n: create_or_get_author())
    complete_status = factory.Sequence(lambda n: random.randint(1, 4))
    ttv_type = factory.Sequence(lambda n: get_ttv_type(n))
    user = User.objects.all()[0]
