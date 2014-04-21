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
from book.models import Author, Language
import os
from book.features.factories.language_factory import LanguageFactory
from book.models.profile_model import Profile

TOTAL_BOOK_WILL_BE_CREATED = 33


@before.each_scenario
def clear_user_in_db(scenario):
    Profile.objects.filter(user_id__gt=1).delete()
    User.objects.filter(id__gt=1).delete()
    Group.objects.all().delete()
    Book.objects.all().delete()
    Category.objects.all().delete()
    Author.objects.all().delete()

@before.all
def clear_prc_folder():
    os.system("rm -f %s/*" % 'media/books/prc')

