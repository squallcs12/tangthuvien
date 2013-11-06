'''
Created on Aug 9, 2013

@author: antipro
'''
from django.core.management.base import BaseCommand
from optparse import make_option
from book.models.book_model import Book
import datetime
from django.template.loader import render_to_string
from tangthuvien import settings
import subprocess
import codecs
import os
from book.models.attachment_model import Attachment
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class Command(BaseCommand):
    help = """
    Generate prc file for book
    """

    option_list = BaseCommand.option_list + (
        make_option('-b', '--book', action='store', dest='book', default='0',
             help='Book ID from dev.tangthuvien.vn'),
        make_option('-a', '--all', action='store', dest='all', default=0,
             help='Book ID from dev.tangthuvien.vn'),
    )

    def handle(self, *args, **options):
        book_id = int(options.get('book', 0))
        is_all = int(options.get('all', 0))

        if is_all:
            books = Book.objects.all()
        elif book_id:
            books = [Book.objects.get(pk=book_id)]
        else:
            yesterday = datetime.date.today() - datetime.timedelta(1)
            books = Book.objects.filter(last_update__gt=yesterday)

        for book in books:
            assert isinstance(book, Book)
            html_content = render_to_string('book/prc_html_file.phtml', {'book':book})
            with codecs.open(settings.media_path(book.html_file), "w", "utf-8") as fp:
                fp.write(html_content)

        for book in books:
            os.system("%s %s -c2 -o %s" % (
                settings.realpath('program/kindlegen'),
                settings.media_path(book.html_file),
                book.prc_file_name
            ))
            file_size = os.path.getsize(settings.media_path(book.prc_file))
            try:
                attachment = Attachment.objects.get(name=book.prc_file_name)
                attachment.size = file_size
                attachment.creation_date = timezone.now()
            except ObjectDoesNotExist:
                attachment = Attachment(
                                name=book.prc_file_name,
                                file=book.prc_file,
                                uploader=book.user,
                                is_approved=True,
                                book=book,
                                downloads_count=0,
                                size=file_size
                            )
            attachment.save()
