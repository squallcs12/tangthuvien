'''
Created on Jul 28, 2013

@author: antipro
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('thankshop.views',
    url(r'^thank_point/buy/return', 'thank_point_shop.paypal_return', name='thankshop_thank_point_paypal_return'),
    url(r'^thank_point/buy/cancel', 'thank_point_shop.paypal_cancel', name='thankshop_thank_point_paypal_cancel'),
    url(r'^thank_point/buy/(?P<package_id>\d*)', 'thank_point_shop.buy', name='thankshop_thank_point_buy'),
    url(r'^thank_point/', 'thank_point_shop.index', name='thankshop_thank_point_shop'),
)
