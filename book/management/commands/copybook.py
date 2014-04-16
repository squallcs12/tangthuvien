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
from book.utils import simple_bb

class Command(BaseCommand):
    help = """
    Copy book from tangthuvien.vn to dev site
    """

    option_list = BaseCommand.option_list + (
        make_option('-t', '--thread', action='store', dest='thread', default='',
             help='Thread ID from tangthuvien.vn'),
        make_option('-b', '--book', action='store', dest='book', default='',
             help='Book ID from dev.tangthuvien.vn'),
        make_option('-s', '--start', action='store', dest='start', default=1,
             help='Start page'),
        make_option('-p', '--start-post', action='store', dest='start_post', default=0,
             help='Start post index'),
        make_option('-e', '--end', action='store', dest='end', default=0,
             help='End page'),
        make_option('-k', '--skip', action='store', dest='skip', default=1,
             help='Skip first post'),
        make_option('-l', '--log', action='store', dest='log', default='',
             help='Log file'),
    )

    def get_thread_html(self, thread_id, page=1):
        url = 'http://www.tangthuvien.vn/forum/vbb_migration/thread_chapters.php?threadid=%s&code=123qweasdzxc&page=%s' % (thread_id, page)
        response = requests.get(url)
        return response.content

    def get_page_range_from_content(self, content):
        assert isinstance(content, BeautifulSoup)
        page_nav = content.find('div', class_="pagenav")
        if not page_nav:
            return 1, 1
        summary = page_nav.find("td", class_="vbmenu_control")
        start, end = summary.text.split(' ')[1].split('/')
        return int(start), int(end)


    def handle(self, *args, **options):
        thread_id = (options.get('thread', 0))
        book_id = int(options.get('book', 0))
        start = int(options.get('start', 1))
        start_post = int(options.get('start_post', 0))
        end = int(options.get('end', 0))
        log = options.get('log', '')
        self.skip = options.get('skip') == 1
        if not log:
            for message in self.copy(thread_id, book_id, start, end, start_post):
                print message
        else:
            with open(log, "w+") as fb:
                pass
            for message in self.copy(thread_id, book_id, start, end, start_post):
                with open(log, "a") as fb:
                    fb.write("\n%s" % message)

    def copy(self, thread_id, book_id, start, end, start_post):
        if not thread_id or not book_id:
            sys.stdout.write("You must specific thread and book")

        post_count = 0
        page = 1

        book = Book.objects.get(pk=book_id)

        chapter_number = 1
        try:
            copy_log = Copy.objects.get(thread_id=thread_id)

            if not copy_log.is_done:  # other process are running
                return

            copy_log.is_done = False
        except ObjectDoesNotExist:
            copy_log = Copy(book=book, thread_id=thread_id, last_chapter_number=chapter_number, last_page=page, last_post=post_count, is_done=False)
        copy_log.save()

        end = int(self.get_thread_html(thread_id, 0))

        yield "start %s" % start
        yield "end %s" % end
        yield ""

        language = book.languages.all()[0]

        for page in range(start, end + 1):
            yield "process_page %s" % page
            content = self.get_thread_html(thread_id, page)
            posts = json.loads(content)

            post_count = 0

            if start_post:
                post_count = start_post
            elif self.skip:
                post_count += 1
                self.skip = False

            if post_count:
                posts = posts[post_count:]

            yield "total_chapter %s" % len(posts)
            for post in posts:
                post_count += 1

                post_content = post['pagetext']

                if not post_content:  # deleted post
                    continue

                spoiler_end = post_content.find("[/SPOILER]")
                if spoiler_end == -1:
                    yield "skip_post %s" % post_count
                    continue

                spoiler_start = post_content.rfind("[SPOILER", 0, spoiler_end)
                spoiler_start = post_content.find(']', spoiler_start) + 1

                vp = post_content[spoiler_start:spoiler_end]

                username = post['username']

                try:
                    user = User.objects.get(username=username)
                except:
                    email = requests.get(
                                "http://www.tangthuvien.vn/forum/vbb_migration/user_email.php",
                                params={'username': username, 'code': '123qweasdzxc'}
                            ).content
                    user = User.objects.create_user(username, email, settings.TEST_PASSWORD)

                yield "process_chapter %s" % chapter_number
                chapter = Chapter()
                chapter.content = "".join(["<p>%s</p>" % txt.strip() for txt in simple_bb(vp).split("\n") if txt])
                chapter.number = book.chapters_count + 1
                chapter.book = book
                chapter.user = user
                chapter.language = language
                chapter.save()
                chapter_number += 1

                copy_log.last_chapter_number = chapter_number
                copy_log.last_page = page
                copy_log.last_post = post_count
                copy_log.is_done = True
                copy_log.save()
            yield "finish_page %s" % page
            yield ""

        yield "finish"
