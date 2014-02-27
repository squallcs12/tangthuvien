
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