from thankshop.models import Item
import factory


class ItemFactory(factory.Factory):
    FACTORY_FOR = Item

    name = factory.Sequence(lambda n: 'Author {0}'.format(n))
    short_description = factory.Sequence(lambda n: 'author-{0}'.format(n))
    long_description = factory.Sequence(lambda n: 'author-{0}'.format(n))
    price = factory.Sequence(lambda n: n * 100 + 100)
    stocks = factory.Sequence(lambda n: n + 1)
