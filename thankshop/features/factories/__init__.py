from thankshop.models import Item, Package
import factory


class ItemFactory(factory.Factory):
    FACTORY_FOR = Item

    name = factory.Sequence(lambda n: 'Item {0}'.format(n))
    short_description = factory.Sequence(lambda n: 'item-{0}'.format(n))
    long_description = factory.Sequence(lambda n: 'item-{0}'.format(n))
    price = factory.Sequence(lambda n: n * 100 + 100)
    stocks = factory.Sequence(lambda n: n + 1)

class ThankFactory(factory.Factory):
    FACTORY_FOR = Package

    name = factory.Sequence(lambda n: 'Package {0}'.format(n))
    price = factory.Sequence(lambda n: n * 100 + 100)
    points = factory.Sequence(lambda n: n * 200 + 200)
    sku = factory.Sequence(lambda n: "sku-%s" % n)
