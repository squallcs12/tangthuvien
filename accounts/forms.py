'''
Created on Sep 16, 2013

@author: antipro
'''
from django.contrib.auth import forms

class AuthenticationForm(forms.AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(AuthenticationForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class PasswordChangeForm(forms.PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
