from django.contrib import admin
from book import models
from book.admin.book_admin import BookAdmin
from book.admin.chapter_admin import ChapterAdmin
from book.admin.author_admin import AuthorAdmin
from book.admin.attachment_admin import AttachmentAdmin

admin.site.register(models.Attachment, AttachmentAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookType)
admin.site.register(models.Category)
admin.site.register(models.Chapter, ChapterAdmin)
admin.site.register(models.ChapterThank)
admin.site.register(models.ChapterType)
admin.site.register(models.Favorite)
admin.site.register(models.Rating)
admin.site.register(models.RatingLog)
admin.site.register(models.Type)
admin.site.register(models.UserLog)
