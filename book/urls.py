'''
Created on Jul 28, 2013

@author: antipro
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('book.views',
    url(r'^$', 'index_view.main', name='books_home'),
    url(r'^submit_thank', 'thank_view.main', name='summit_thank_request'),
    url(r'^submit_book_rating', 'rating_view.main', name='submit_book_rating'),
    url(r'^submit_favorite_book', 'favorite_view.ajax_submit', name='submit_favorite_book'),
    url(r'^unfavorite_books', 'favorite_view.unfavorite_books', name='unfavorite_books'),
    url(r'^favorite', 'favorite_view.main', name='favorite_books'),
    url(r'^post_new_chapter/(?P<book_id>\d*)', 'post_new_chapter_view.main', name='post_new_chapter'),
    url(r'^s/(?P<book_id>\d*)', 'book_read.short', name='book_read_short'),
    url(r'^(?P<slug>.*)$', 'book_read.main', name='book_read'),
)
