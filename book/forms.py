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
from tangthuvien.functions import UserSettings
from tangthuvien import settings

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

        return chapter

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
    cover = forms.ImageField(required=False)
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


class ConfigReadingSectionForm(forms.Form):
    font_family = forms.ChoiceField(
                    widget=forms.Select(attrs={'data-css-name':'font-family'}),
                    choices=[('', '---'), ('Arial', 'Arial'), ('Tahoma', 'Tahoma'), ]
                    )
    font_size = forms.ChoiceField(
                    widget=forms.Select(attrs={'data-css-name':'font-size'}),
                    choices=[('', '---'), ('20px', '20px'), ('30px', '30px'), ]
                    )

    def __init__(self, user, *args, **kwargs):
        super(ConfigReadingSectionForm, self).__init__(*args, **kwargs)
        self.user = user
        self._styles = -1
        styles = self.styles
        if styles:
            for style in styles.split(';'):
                style_name, style_value = style.split(':')
                for boundfield in self:
                    if boundfield.field.widget.attrs['data-css-name'] == style_name:
                        boundfield.field.initial = style_value

    def process(self):
        styles = []
        for boundfield in self:
            styles.append("%s:%s" % (boundfield.field.widget.attrs['data-css-name'], boundfield.value()))
        UserSettings.set(settings.REDIS_READING_BOOK_STYLE_KEY, self.user.id, ";".join(styles))

    @property
    def styles(self):
        if self._styles != -1:
            return self._styles
        self._styles = UserSettings.get(settings.REDIS_READING_BOOK_STYLE_KEY, self.user.id)
        return self._styles

