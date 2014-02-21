from lettuce_setup.function import *  # @UnusedWildImport
from book.models import Attachment
import os
from book.models.book_model import Book


def get_attachments_list():
    return [attachment.text for attachment in find_all("#attachments .filename")]

def read_book_by_id(book_id):
    visit_by_view_name('book_read_short', kwargs={'book_id':book_id})

@step(u'I upload a attachment to the book')
def i_upload_a_attachment_to_the_book(step):
    until(lambda: not find("#upload_attachment .progress").is_displayed())
    upload_form = find("#upload_attachment")
    upload_form.find(".upload").send_keys(os.path.join(settings.MEDIA_ROOT, "books/covers/1278231576904.jpg"))
    time.sleep(0.5)
    if find("#upload_attachment .progress").is_displayed():
        until(lambda: not find("#upload_attachment .progress").is_displayed())

@step(u'I see the attachment listed when reading that book')
def i_see_the_attachment_listed_when_reading_that_book(step):
    get_attachments_list().should.contain("1278231576904.jpg")

@step(u'the attachment can not be seen by other normal user')
def the_attachment_can_not_be_seen_by_other_normal_user(step):
    visit_by_view_name("logout")
    read_book_by_id(world.book_id)
    get_attachments_list().should_not.contain("1278231576904.jpg")
    given_i_was_a_logged_in_user(step)
    read_book_by_id(world.book_id)

@step(u'I reach the limited of uploading attachment')
def i_reach_the_limited_of_uploading_attachment(step):
    profile = default_user().book_profile
    profile.daily_uploaded_attachments_count = settings.BOOK_ATTACHMENTS_COUNT_UPLOAD_LIMIT
    profile.save()

@step(u'I can not upload attachment anylonger')
def i_can_not_upload_attachment_anylonger(step):
    when_i_reload_the_page(step)
    find("#attachments .upload").tag_name.should_not.equal("input")

@step(u'the attachment can be seen by other normal user')
def the_attachment_can_be_seen_by_other_normal_user(step):
    visit_by_view_name("logout")
    read_book_by_id(world.book_id)
    get_attachments_list().should.contain("1278231576904.jpg")
    given_i_was_a_logged_in_super_user(step)

@step(u'I approve that attachment')
def i_approve_that_attachment(step):
    find("#attachments .approve").click()

@step(u'I reach the limited of approving attachment')
def i_reach_the_limited_of_approving_attachment(step):
    profile = default_user(3).book_profile
    profile.daily_approved_attachments_count = settings.BOOK_ATTACHMENTS_COUNT_APPROVE_LIMIT
    profile.save()

@step(u'I can not approve attachment anylonger')
def i_can_not_approve_attachment_anylonger(step):
    for attachment in world.book.attachment_set.all():
        attachment.is_approved = False
        attachment.save()

    read_book_by_id(world.book_id)
    len(find_all("#attachments .filename")).should_not.equal(0)
    len(find_all("#attachments .approve")).should.equal(0)

@step(u'I can download the attachment')
def i_can_download_the_attachment(step):
    len(find_all("#attachments a")).should_not.equal(0)

@step(u'I reach the limited of downloading attachment')
def i_reach_the_limited_of_downloading_attachment(step):
    profile = default_user().book_profile
    profile.daily_downloaded_attachments_count = settings.BOOK_ATTACHMENTS_COUNT_DOWNLOAD_LIMIT
    profile.save()

@step(u'I can not download attachment anylonger')
def i_can_not_download_attachment_anylonger(step):
    read_book_by_id(world.book_id)
    len(find_all("#attachments a")).should.equal(0)

@step(u'I read a book has( approved)? attachment uploaded by normal user')
def i_read_a_book_has_approved_attachment_uploaded_by_normal_user(step, approved):
    book = Book.objects.all()[0]
    Attachment.objects.create(
                        uploader=default_user(),
                        book=book,
                        name='1278231576904.jpg',
                        file='media/books/attachments/1278231576904.jpg',
                        size=102400,
                        is_approved=bool(approved),
                        downloads_count=0,
                    )
    world.book_id = book.id
    world.book = book
    read_book_by_id(book.id)
