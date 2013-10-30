import factory
from book.models import ChapterType
class ChapterTypeFactory(factory.Factory):

    FACTORY_FOR = ChapterType
    name = factory.Sequence(lambda n : "chapter-type-{0}".format(n))
