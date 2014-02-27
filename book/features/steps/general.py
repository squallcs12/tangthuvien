
def current_book():
    from lettuce_setup.function import db_commit, world
    from book.models import Book
    db_commit()
    return Book.objects.get(pk=world.book_id)