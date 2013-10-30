'''
Created on Jul 28, 2013

@author: antipro
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('book.views',
    url(r'^$', 'index_view.main', name='books_home'),
    url(r'^ajax_list_books$', 'index_view.ajax', name='ajax_list_books'),
    url(r'^categories/(?P<slugs>.*)$', 'index_view.by_categories', name='books_list_by_categories'),
    url(r'^submit_thank', 'thank_view.main', name='summit_thank_request'),
    url(r'^submit_book_rating', 'rating_view.main', name='submit_book_rating'),
    url(r'^submit_favorite_book', 'favorite_view.ajax_submit', name='submit_favorite_book'),
    url(r'^unfavorite_books', 'favorite_view.unfavorite_books', name='unfavorite_books'),
    url(r'^favorite', 'favorite_view.main', name='favorite_books'),
    url(r'^post_new_chapter/(?P<book_id>\d*)', 'post_new_chapter_view.main', name='post_new_chapter'),
    url(r'^publish', 'publish_new_book_view.main', name='publish_new_book'),
    url(r'^add_book_author_ajax', 'add_book_author_view.ajax', name='add_book_author_ajax'),
    url(r'^add_book_type_ajax', 'add_book_type_view.ajax', name='add_book_type_ajax'),
    url(r'^ajax_book_reading_config', 'book_reading_config_view.ajax', name='ajax_book_reading_config'),
    url(r'^upload_book_attachment_ajax/(?P<book_id>\d*)', 'attachment_upload_view.ajax', name='upload_book_attachment_ajax'),
    url(r'^approve_book_attachment_ajax', 'attachment_approve_view.ajax', name='approve_book_attachment_ajax'),
    url(r'^book_attachment_download/(?P<book_id>\d*)/(?P<attachment_id>\d*)', 'attachment_download_view.main', name='book_attachment_download'),
    url(r'^copy_book$', 'copy_book_view.main', name='copy_book'),
    url(r'^copy_book_process/(?P<book_id>\d*)', 'copy_book_view.process', name='copy_book_process'),
    url(r'^copy_book_process_output/(?P<book_id>\d*)', 'copy_book_view.process_output', name='copy_book_process_output'),
    url(r'^s/(?P<book_id>\d*)', 'book_read.short', name='book_read_short'),
    url(r'^(?P<slug>[^/]+)/(?P<chapter_number>\d+)$', 'book_read.chapter', name='read_book_chapter'),
    url(r'^(?P<slug>[^/]+)$', 'book_read.main', name='book_read'),
)
