'''
Created on Sep 21, 2013

@author: antipro
'''
from django import forms
from django.utils.translation import ugettext as _
from book.models import Chapter, Language
from book.models.chapter_model import Chapter
from book.models import Author
from ckeditor.widgets import CKEditorWidget
from book.models.book_model import Book
from tangthuvien.functions import UserSettings
from tangthuvien import settings
from django.contrib import messages
from book.models.copy_model import Copy
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class PostNewChapterForm(forms.ModelForm):

    def __init__(self, book, user, *args, **kwargs):
        super(PostNewChapterForm, self).__init__(*args, **kwargs)
        self.fields['book'].initial = book.id
        self.fields['user'].initial = user.id
        self.fields['user'].editable = False
        self.fields['book'].editable = False

    class Meta:
        model = Chapter
        fields = ['book', 'user', 'title', 'number', 'content', 'language']
        widgets = {
            'book': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }

class EditChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'number', 'content']

class AddAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddAuthorForm, self).__init__(*args, **kwargs)
        self.fields['information'].required = False
        self.fields['information'].widget = forms.Textarea()
    class Meta:
        model = Author
        fields = ['name', 'information']

class AddLanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']

class PublishNewBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['user', 'title', 'description', 'cover', 'author', 'languages']
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(PublishNewBookForm, self).__init__(*args, **kwargs)
        self.fields['user'].editable = False
        self.fields['user'].initial = user.id
        self.fields['cover'].required = False

class CopyBookForm(PublishNewBookForm):
    thread_url = forms.URLField()
    skip_first_post = forms.BooleanField(required=False)

    def clean_thread_url(self):
        thread_id = self.cleaned_data['thread_url'].split('?')[1].split('=')[1]  # last param number
        if Copy.objects.filter(thread_id=thread_id).exists():
            raise ValidationError(_("The book is already copied to this site."))
        return self.cleaned_data['thread_url']

style_font_size_choices = [(item, item) for item in settings.BOOK_READING_STYLE_FONT_SIZES]
style_font_size_choices.insert(0, ('', '---'))
style_font_family_choices = [(item, item) for item in settings.BOOK_READING_STYLE_FONT_FAMILIES]
style_font_family_choices.insert(0, ('', '---'))

class ConfigReadingSectionForm(forms.Form):
    font_family = forms.ChoiceField(
                    widget=forms.Select(attrs={'data-css-name':'font-family'}),
                    choices=style_font_family_choices,
                    required=False,
                    )
    font_size = forms.ChoiceField(
                    widget=forms.Select(attrs={'data-css-name':'font-size'}),
                    choices=style_font_size_choices,
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

