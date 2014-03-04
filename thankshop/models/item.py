'''
Created on Dec 14, 2013

@author: antipro
'''
from django.db import models
from thankshop import exceptions
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.utils import IntegrityError
from ckeditor.fields import RichTextField
from django.conf import settings

class Item(models.Model):
    name = models.CharField(max_length=255)
    short_description = RichTextField()
    long_description = RichTextField()
    price = models.IntegerField(_("Price (Thanks)"))
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

    def image_html(self):
        image_url = "%s%s" % (settings.MEDIA_URL, self.image)
        return "<a href=\"%s\" target=\"_blank\"><img src=\"%s\" height=\"100px\" /></a>" % (image_url, image_url)
    image_html.allow_tags = True
    image_html.short_description = _("Image")

    def __unicode__(self):
        return self.name


class UserItem(models.Model):
    user = models.ForeignKey(User, related_name="thankshop_items")
    item = models.ForeignKey('thankshop.Item')

    class Meta:
        app_label = "thankshop"
        unique_together = (("user", "item"),)
