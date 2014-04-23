def current_book():
    from lettuce_setup.function import db_commit, world
    from book.models import Book
    db_commit()
    return Book.objects.get(pk=world.book_id)

def get_attachments_list():
    from lettuce_setup.function import find_all
    return [attachment.text for attachment in find_all("#attachments .filename")]

def read_book_by_id(book_id):
    from lettuce_setup.function import visit_by_view_name
    visit_by_view_name('book_read_short', kwargs={'book_id':book_id})

def author():
    from lettuce import world
    from book.models.author_model import Author
    from book.features.factories.author_factory import AuthorFactory
    if not hasattr(world, "author"):
        try:
            world.author = Author.objects.all()[0]
        except IndexError:
            world.author = AuthorFactory()
            world.author.save()
    return world.author

def language():
    from lettuce import world
    if not hasattr(world, "language"):
        try:
            from book.models.language_model import Language
            world.language = Language.objects.all()[0]
        except IndexError:
            from book.features.factories.language_factory import LanguageFactory
            world.language = LanguageFactory()
            world.language.save()
    return world.language

def category():
    from lettuce import world
    if not hasattr(world, "category"):
        try:
            from book.models.category_model import Category
            world.category = Category.objects.all()[0]
        except IndexError:
            from book.features.factories.category_factory import CategoryFactory
            world.category = CategoryFactory()
            world.category.save()
    return world.category
