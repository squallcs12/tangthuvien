'''
Created on Aug 9, 2013

@author: antipro
'''
from django.core.management.base import BaseCommand
from optparse import make_option
from book.models.chapter_model import Chapter
from book.utils import simple_bb
from book.models.book_model import Book

class Command(BaseCommand):
    help = """
    Copy book from tangthuvien.vn to dev site
    """

    option_list = BaseCommand.option_list + (
        make_option('-b', '--book', action='store', dest='book', default=0,
             help='Book ID'),
        make_option('-c', '--chapter', action='store', dest='chapter', default=0,
             help='Chapter ID'),
    )

    def handle(self, *args, **options):
        book_id = options.get('book', 0)
        chapter_id = options.get('chapter', 0)

        if chapter_id:
            chapter = Chapter.objects.get(pk=int(chapter_id))
            chapter.content = simple_bb(chapter.content)
            chapter.save()

        if book_id:
            books = [Book.objects.get(pk=int(book_id))]
        else:
            books = Book.objects.all()

        for book in books:
            for chapter in book.chapter_set.all():
                chapter.content = simple_bb(chapter.content)
                chapter.save()
                print "BOOK_ID %s CHAPTER_ID %s" % (book.id, chapter.id)

        print "DONE"
