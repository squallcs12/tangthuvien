from django.contrib import admin
from book.models import Book, ChapterType, Author, Category, BookType, Chapter
from book.admin.book_admin import BookAdmin
from book.admin.chapter_admin import ChapterAdmin
from book.admin.author_admin import AuthorAdmin

admin.site.register(Book, BookAdmin)
admin.site.register(ChapterType)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookType)
admin.site.register(Category)
admin.site.register(Chapter, ChapterAdmin)
