'''
Created on Jul 28, 2013

@author: antipro
'''
from book.models import Book, Author, BookType
import factory
from book.features.factories.author_factory import AuthorFactory
import random
from django.contrib.auth.models import User
from book.features.factories.booktype_factory import BookTypeFactory

def get_random_type(n):
    return BookType.objects.all()[n % 3]

def get_ttv_type(n):
    try:
        return get_random_type(n)
    except IndexError:
        for i in range(0, 3):  # @UnusedVariable
            BookTypeFactory().save()
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
    #cover = "books/covers/1278231576904.jpg"
    description = factory.Sequence(lambda n: '''
        {0}
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam adipiscing dapibus orci ut fermentum. Ut in felis vehicula, imperdiet justo in, laoreet tellus. Nam porta lorem sed lorem elementum, at elementum dolor cursus. Nam nec gravida nulla. In justo urna, congue eget lectus hendrerit, tempus iaculis tellus. Nulla interdum neque id ante placerat iaculis. Aliquam tincidunt orci vel tincidunt mattis. Cras vestibulum aliquet nisl, ac suscipit elit pulvinar id. Duis eget commodo risus. Maecenas pellentesque libero eu turpis feugiat luctus. Duis convallis at massa et ornare. Cras venenatis, turpis eu bibendum interdum, augue augue dignissim libero, vitae aliquet erat nibh vel enim. Vestibulum non risus nec lacus vestibulum commodo in id enim. Suspendisse at tincidunt sapien. Proin a faucibus diam, pulvinar dignissim massa. In hac habitasse platea dictumst.
    '''.format(n))
