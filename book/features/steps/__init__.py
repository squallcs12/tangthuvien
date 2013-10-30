from lettuce_setup.function import *  # @UnusedWildImport
from django.contrib.auth.models import Group
from book.models.attachment_model import Attachment
from book.features.factories.book_factory import BookFactory
from book.features.factories.chapter_factory import ChapterFactory
from book.features.factories.chapter_type_factory import ChapterTypeFactory
from book.features.factories.category_factory import CategoryFactory
import random
from book.models.category_model import Category
import subprocess
from tangthuvien import settings as st
from book.models.book_model import Book
from book.models import Author, BookType
import os

TOTAL_BOOK_WILL_BE_CREATED = 33


@before.all
def clear_user_in_db():
    for user in User.objects.filter(id__gt=1):
        user.delete()
    for group in Group.objects.all():
        group.delete()

@before.all
def clear_prc_folder():
    os.system("rm -f %s/*" % 'media/books/prc')

@before.all
def add_super_group_permission():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(Attachment)
    group = super_group()
    can_approve_attachment = Permission.objects.get(codename='can_approve_attachment', content_type=content_type)
    try:
        group.permissions.add(can_approve_attachment)
    except:
        pass

@before.each_feature
def before_book_feature(feature):
    if ('Book App ::' in feature.name) and \
        (not hasattr(world, 'book_created') or not world.book_created):
        create_book_list()

def clean_book_tables():
    for book in Book.objects.all():
        book.delete()
    for category in Category.objects.all():
        category.delete()
    for author in Author.objects.all():
        author.delete()
    for book_type in BookType.objects.all():
        book_type.delete()

def create_book_list():
    clean_book_tables()
    world.book_created = True
    world.book_list = []

    chappter_types = []
    chappter_type = ChapterTypeFactory()
    chappter_type.save()
    chappter_types.append(chappter_type)
    for i in range(0, TOTAL_BOOK_WILL_BE_CREATED):  # @UnusedVariable
        book = BookFactory()
        book.save()
        world.book_list.append(book)
        for i in range(1, 15 if i > (TOTAL_BOOK_WILL_BE_CREATED - 15) else 2):
            chapter = ChapterFactory()
            chapter.number = i
            chapter.book = book
            chapter.chapter_type = chappter_type
            chapter.user = book.user
            chapter.save()

    for i in range(0, 4):
        category = CategoryFactory()
        category.save()
        assert isinstance(category, Category)
        for book in world.book_list:
            if random.randint(0, 1):
                category.books.add(book)
    
    subprocess.call(['rm',  '%s/*' % st.realpath('log/copybook'), '-f'])