'''
Created on Sep 21, 2013

@author: antipro
'''
from django import forms
from django.utils.translation import ugettext_lazy as _
from book.models.chapter_model import Chapter
from book.models import ChapterType

class PostNewChapterForm(forms.Form):
    title = forms.CharField(max_length=255)
    number = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea)
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
