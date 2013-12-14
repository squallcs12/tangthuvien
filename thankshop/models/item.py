'''
Created on Dec 14, 2013

@author: antipro
'''
from django.db import models
from thankshop import exceptions
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.utils import IntegrityError

class Item(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    long_description = models.TextField()
    price = models.IntegerField()
    stocks = models.IntegerField()
    image = models.ImageField(upload_to='thankshop/item_images/')

    class Meta:
        app_label = 'thankshop'

    @classmethod
    def sell(cls, user, item_id):
        item = cls.objects.get(pk=item_id)
        assert isinstance(item, Item)

        if item.stocks == 0:
            raise exceptions.ItemStockNotAvailableException(_("Item not found in stock."))

        thank_obj = user.thank_point
        if item.price > thank_obj.thanked_points:
            raise exceptions.NotEnoughThankedPointsException(_("You don't have enough thanked points."))
        try:
            UserItem(user=user, item=item).save()
            thank_obj.increase_thanked_points(-item.price, "buy_item_%s" % item.id)
        except IntegrityError:
            raise exceptions.AlreadyOwnItemException(_("This item is already owned by you."))
        return item


class UserItem(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey('thankshop.Item')

    class Meta:
        app_label = "thankshop"
        unique_together = (("user", "item"),)
