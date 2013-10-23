'''
Created on Sep 16, 2013

@author: antipro
'''
from django import forms
from django.contrib.auth import forms as auth_form, authenticate
from django.utils.translation import ugettext_lazy as _
import requests
from django.contrib.auth.models import User
import json

class AuthenticationForm(auth_form.AuthenticationForm):

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None:
                live_verify_url = 'http://www.tangthuvien.vn/forum/vbb_migration/verify_user_login.php?username=%s&password=%s'
                verify_result = requests.get(live_verify_url % (username, password)).content
                if verify_result != '0':  # verify success
                    user_data = json.loads(verify_result)
                    User.objects.create_user(username, user_data['email'], password)
                    self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'] % {
                        'username': self.username_field.verbose_name
                    })
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data
