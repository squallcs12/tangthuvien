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
import pdb

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
        make_option('-e', '--end', action='store', dest='end', default=0,
             help='End page'),
        make_option('-k', '--skip', action='store', dest='skip', default=1,
             help='Skip first post'),
    )

    def get_thread_html(self, thread_id, page=1):
        url = 'http://www.tangthuvien.vn/forum/showthread.php?t=%s&page=%s' % (thread_id, page)
        response = requests.get(url)
        return response.content

    def get_page_range_from_content(self, content):
        assert isinstance(content, BeautifulSoup)
        summary = content.find('div', class_="pagenav").find("td", class_="vbmenu_control")
        start, end = summary.text.split(' ')[1].split('/')
        return int(start), int(end)


    def handle(self, *args, **options):

        thread_id = int(options.get('thread', 0))
        book_id = int(options.get('book', 0))
        start = int(options.get('start', 1))
        end = int(options.get('end', 0))


        if not thread_id or not book_id:
            print("You mush specific thread and book")

        book = Book.objects.get(pk=book_id)

        content = self.get_thread_html(thread_id, start)
        content = BeautifulSoup(content)
        thread_start, thread_end = self.get_page_range_from_content(content)
        if start < thread_start or start > thread_end:
            start = thread_start
        if end < thread_start or end > thread_end:
            end = thread_end

        chapter_number = 1
        skip = True
        for page in range(start, end + 1):
            print("Copy page %s" % page)
            content = self.get_thread_html(thread_id, page)

            start_posts_index = content.find('<div id="posts">') + len('<div id="posts">')
            end_posts_index = content.find('<div id="lastpost">')
            posts = content[start_posts_index: end_posts_index]
            posts = posts.split("<!-- / close content container -->")[0:-1]

            post_count = 0
            for post in posts:
                post_count += 1
                if skip:
                    skip = False
                    continue

                post = BeautifulSoup(post)
                vp = post.find(class_="hiddentext")

                if not vp:
                    print("There is no VP in post %s from url http://www.tangthuvien.vn/forum/showthread.php?t=%s&page=%s" % (post_count, thread_id, page))
                    enter = raw_input("Please check. Continue? [y]/n")
                    if enter == 'n':
                        exit()
                    continue
                print("Copy chapter %s" % chapter_number)
                chapter = Chapter()
                chapter.content = "".join(["<p>%s</p>" % txt.strip() for txt in vp.text.split("\n") if txt])
                chapter.number = chapter_number
                chapter.book = book
                chapter.user = book.user
                chapter.chapter_type_id = 1
                chapter.save()
                chapter_number += 1
            print("Finish page %s" % page)
            print("")

        print "Finish"
