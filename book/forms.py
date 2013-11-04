'''
Created on Sep 21, 2013

@author: antipro
'''
from django import forms
from django.utils.translation import ugettext as _
from book.models import Chapter
from book.models.chapter_model import Chapter
from book.models import ChapterType, Author, BookType
from ckeditor.widgets import CKEditorWidget
from book.models.book_model import Book
from tangthuvien.functions import UserSettings
from tangthuvien import settings
from django.contrib import messages
from book.models.copy_model import Copy
from django.core.exceptions import ObjectDoesNotExist

class PostNewChapterForm(forms.ModelForm):

    def __init__(self, book, user, *args, **kwargs):
        super(PostNewChapterForm, self).__init__(*args, **kwargs)
        self.fields['book'].initial = book.id
        self.fields['user'].initial = user.id
        self.fields['user'].editable = False
        self.fields['book'].editable = False

    class Meta:
        model = Chapter
        fields = ['book', 'user', 'title', 'number', 'content', 'chapter_type']
        widgets = {
            'book': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }

class EditChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'number', 'content']

class AddAuthorForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(AddAuthorForm, self).__init__(*args, **kwargs)
        self.fields['information'].required = False
    class Meta:
        model = Author
        fields = ['name', 'information']

class AddBookTypeForm(forms.ModelForm):
    class Meta:
        model = BookType
        fields = ['name']
    name = forms.CharField()

class PublishNewBookForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=CKEditorWidget())
    cover = forms.ImageField(required=False)
    author = forms.ModelChoiceField(queryset=Author.objects.order_by('name'))
    ttv_type = forms.ModelChoiceField(queryset=BookType.objects.order_by('name'))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PublishNewBookForm, self).__init__(*args, **kwargs)

    def process(self):
        book = Book()
        book.user = self.request.user
        for key, value in self.cleaned_data.items():
            setattr(book, key, value)
        book.save()

        messages.success(self.request, _("New book was published successfully."))

        return book

class CopyBookForm(PublishNewBookForm):
    thread_url = forms.URLField()

    def is_valid(self):
        is_valid = super(CopyBookForm, self).is_valid()
        if is_valid:
            thread_id = self.cleaned_data['thread_url'].split('?')[1].split('=')[1]  # last param number
            if Copy.objects.filter(thread_id=thread_id).exists():
                messages.error(self.request, _("The book is already copied to this site."))
                return False
        return is_valid


class ConfigReadingSectionForm(forms.Form):
    font_family = forms.ChoiceField(
                    widget=forms.Select(attrs={'data-css-name':'font-family'}),
                    choices=[('', '---'), ('Arial', 'Arial'), ('Tahoma', 'Tahoma'), ],
                    required=False,
                    )
    font_size = forms.ChoiceField(
                    widget=forms.Select(attrs={'data-css-name':'font-size'}),
                    choices=[('', '---'), ('20px', '20px'), ('30px', '30px'), ],
                    required=False
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

