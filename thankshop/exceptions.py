'''
Created on Dec 14, 2013

@author: antipro
'''

class ShopException(Exception):
    pass

class ItemStockNotAvailableException(ShopException):
    pass

class NotEnoughThankedPointsException(ShopException):
    pass
