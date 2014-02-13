'''
Created on Jul 28, 2013

@author: antipro
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('thankshop.views',
    url(r'^thank_point/buy/return', 'thank_point_shop_view.paypal_return', name='thankshop_thank_point_paypal_return'),
    url(r'^thank_point/buy/cancel', 'thank_point_shop_view.paypal_cancel', name='thankshop_thank_point_paypal_cancel'),
    url(r'^thank_point/buy/(?P<package_id>\d*)', 'thank_point_shop_view.buy', name='thankshop_thank_point_buy'),
    url(r'^thank_point/', 'thank_point_shop_view.index', name='thankshop_thank_point_shop'),
    url(r'^$', 'shop_homepage_view.index', name='thankshop_shop_homepage'),
    url(r'^buy', 'thankshop_buy_item_view.ajax', name='thankshop_buy_item_ajax'),
    url(r'^inventory/(?P<username>.*)/$', 'thankshop_user_inventory_view.index', name='thankshop_user_inventory'),
    url(r'^inventory/(?P<user_id>.+)/list$', 'thankshop_user_inventory_view.list_items', name='thankshop_user_inventory_list_items'),
)
