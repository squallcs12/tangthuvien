'''
Created on Aug 9, 2013

@author: antipro
'''
from django.core.management.base import BaseCommand
from optparse import make_option
from book.models.book_model import Book
import requests
from bs4 import BeautifulSoup
from book.models.chapter_model import Chapter
import sys
from django.contrib.auth.models import User
from tangthuvien import settings
from book.models.copy_model import Copy
from django.core.exceptions import ObjectDoesNotExist
import json
from book.models.language_model import Language
from django.core.management import call_command
from book.models.author_model import Author

class Command(BaseCommand):
    help = """
    Copy book from tangthuvien.vn to dev site
    """

    option_list = BaseCommand.option_list + (
        make_option('-f', '--forumid', action='store', dest='forumid', default=0,
             help='FORUM ID from tangthuvien.vn'),
    )

    def get_threads(self, page):
        url = 'http://www.tangthuvien.vn/forum/vbb_migration/forum_thread.php?fid=%s&p=%s&code=123qweasdzxc' % (self.forumid, page)
        response = requests.get(url)
        return json.loads(response.content)

    def handle(self, *args, **options):
        self.forumid = (options.get('forumid', 0))

        user = User.objects.all()[0]
        language = Language.objects.all()[0]
        author = Author.objects.all()[0]

        page = 0
        while True:
            page += 1
            threads = self.get_threads(page)

            # copy all
            if len(threads) == 0:
                break

            for thread in threads:
                book = Book()
                book.title = thread['title']
                book.user = user
                book.author = author
                book.save()

                book.languages.add(language)
                book.save()

                call_command("copybook", thread=int(thread['threadid']), book=book.id, skip=0)
