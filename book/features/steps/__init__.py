from lettuce_setup.function import *  # @UnusedWildImport
from django.contrib.auth.models import Group
from book.models.attachment_model import Attachment
from book.features.factories.book_factory import BookFactory
from book.features.factories.chapter_factory import ChapterFactory
from book.features.factories.category_factory import CategoryFactory
import random
from book.models.category_model import Category
import subprocess
from tangthuvien import settings as st
from book.models.book_model import Book
from book.models import Author
import os

TOTAL_BOOK_WILL_BE_CREATED = 33


@before.all
def clear_user_in_db():
    for user in User.objects.filter(id__gt=1):
        user.delete()
    for group in Group.objects.all():
        group.delete()
    for book in Book.objects.all():
        book.delete()

@before.all
def clear_prc_folder():
    os.system("rm -f %s/*" % 'media/books/prc')

def execute_ignore(func):
    try:
        func()
    except:
        pass

@before.all
def add_super_group_permission():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    attachment_content_type = ContentType.objects.get_for_model(Attachment)
    book_content_type = ContentType.objects.get_for_model(Book)
    group = super_group()
    can_approve_attachment = Permission.objects.get(codename='can_approve_attachment', content_type=attachment_content_type)
    can_generate_prc = Permission.objects.get(codename='can_generate_prc', content_type=book_content_type)
    execute_ignore(lambda: group.permissions.add(can_approve_attachment))
    execute_ignore(lambda: group.permissions.add(can_generate_prc))

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

def create_book_list():
    clean_book_tables()
    world.book_created = True
    world.book_list = []

    for i in range(0, 4):
        category = CategoryFactory()
        category.save()
        assert isinstance(category, Category)
        for book in world.book_list:
            if random.randint(0, 1):
                category.books.add(book)

    subprocess.call(['rm', '%s/*' % st.realpath('log/copybook'), '-f'])
