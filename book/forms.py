'''
Created on Sep 21, 2013

@author: antipro
'''
from django import forms
from django.utils.translation import ugettext_lazy as _
from book.models.chapter_model import Chapter
from book.models import ChapterType, Author, BookType
from ckeditor.widgets import CKEditorWidget
from book.models.book_model import Book

class PostNewChapterForm(forms.Form):
    title = forms.CharField(max_length=255)
    number = forms.IntegerField()
    content = forms.CharField(widget=CKEditorWidget())
    chapter_type = forms.ModelChoiceField(queryset=ChapterType.objects)

    def __init__(self, request, book, *args, **kwargs):
        self.request = request
        self.book = book
        super(PostNewChapterForm, self).__init__(*args, **kwargs)

    def process(self):
        chapter = Chapter()
        chapter.book = self.book
        chapter.user = self.request.user
        for key, value in self.cleaned_data.items():
            setattr(chapter, key, value)
        chapter.save()

        self.request.notification.success(_("New chapter was posted successfully."))

class AddAuthorForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(), required=False)

    def process(self):
        author = Author()
        for key, value in self.cleaned_data.items():
            setattr(author, key, value)
        author.save()

        return author

class AddBookTypeForm(forms.Form):
    name = forms.CharField()

    def process(self):
        ttv_type = BookType()
        for key, value in self.cleaned_data.items():
            setattr(ttv_type, key, value)
        ttv_type.save()

        return ttv_type

class PublishNewBookForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=CKEditorWidget())
    cover = forms.ImageField()
    author = forms.ModelChoiceField(queryset=Author.objects.order_by('name'))
    ttv_type = forms.ModelChoiceField(queryset=BookType.objects.order_by('name'))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PublishNewBookForm, self).__init__(*args, **kwargs)
        self.author_form = AddAuthorForm(prefix='author')
        self.type_form = AddBookTypeForm(prefix='type')


    def process(self):
        book = Book()
        book.user = self.request.user
        for key, value in self.cleaned_data.items():
            setattr(book, key, value)
        book.save()

        self.request.notification.success(_("New book was published successfully."))

        return book

class CopyBookForm(PublishNewBookForm):
    thread_url = forms.URLField()

