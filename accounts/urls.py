'''
Created on Jul 30, 2013

@author: antipro
'''
from django.conf.urls import patterns, url, include
from django.contrib.auth.views import login
from accounts.forms import AuthenticationForm, PasswordChangeForm
urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'accounts/login.phtml', 'authentication_form': AuthenticationForm}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name':'accounts/logged_out.phtml'}, name='logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {
            'template_name':'accounts/password_change.phtml',
            'password_change_form': PasswordChangeForm
        }, name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name':'accounts/password_change_done.phtml'}, name='password_change_done'),
    url(r'^password_set/done/$', 'accounts.views.set_password_view.done', name='password_set_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'accounts/password_reset.phtml'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'password_reset_done.phtml'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name':'accounts/password_reset_confirm.phtml'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'accounts/password_reset_complete.phtml'}, name='password_reset_complete'),
    url(r'^profile', 'accounts.views.profile_view.main', name='accounts_profile'),

    url(r'^set_password', 'accounts.views.set_password_view.main', name='set_user_password'),
    url(r'^social_auth/', include('social_auth.urls')),
    url(r'^social', 'accounts.views.social_view.main', name='accounts_social_list')
)
