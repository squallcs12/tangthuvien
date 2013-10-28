from lettuce_setup.function import *  # @UnusedWildImport
from book.models import Attachment
import os

@before.all
def add_super_group_permission():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(Attachment)
    group = super_group()
    can_approve_attachment = Permission.objects.get(codename='can_approve_attachment', content_type=content_type)
    group.permissions.add(can_approve_attachment)

def get_attachments_list():
    return [attachment.text for attachment in find_all("#attachments .filename")]

def read_book_by_id(book_id):
    visit_by_view_name('book_read_short', kwargs={'book_id':book_id})

@step(u'And I upload a attachment to the book')
def and_i_upload_a_attachment_to_the_book(step):
    upload_form = find("#upload_attachment")
    upload_form.find(".upload").send_keys(os.path.join(settings.MEDIA_ROOT, "books/covers/1278231576904.jpg"))
    upload_form.find("[type='submit']").click()

@step(u'Then I see the attachment listed when reading that book')
def then_i_see_the_attachment_listed_when_reading_that_book(step):
    get_attachments_list().should.contain("1278231576904.jpg")

@step(u'And the attachment can not be seen by other normal user')
def and_the_attachment_can_not_be_seen_by_other_normal_user(step):
    visit_by_view_name("logout")
    read_book_by_id(world.book_id)
    get_attachments_list().should_not.contain("1278231576904.jpg")

@step(u'When I reach the limited of uploading attachment')
def when_i_reach_the_limited_of_uploading_attachment(step):
    given_i_was_a_logged_in_user()
    default_user().book_profile.daily_uploaded_attachments_count = settings.BOOK_ATTACHMENTS_COUNT_UPLOAD_LIMIT
    default_user().book_profile.save()

@step(u'Then I can not upload attachment anylonger')
def then_i_can_not_upload_attachment_anylonger(step):
    when_i_reload_the_page()
    find("#attachment .upload").get_attribute('disabled').should_not.be.ok

@step(u'And the attachment can be seen by other normal user')
def and_the_attachment_can_be_seen_by_other_normal_user(step):
    assert False, 'This step must be implemented'
@step(u'And I approve that attachment')
def and_i_approve_that_attachment(step):
    assert False, 'This step must be implemented'
@step(u'Then the attachment can be seen by other normak user')
def then_the_attachment_can_be_seen_by_other_normak_user(step):
    assert False, 'This step must be implemented'
@step(u'When I reach the limited of approving attachment')
def when_i_reach_the_limited_of_approving_attachment(step):
    assert False, 'This step must be implemented'
@step(u'Then I can not approve attachment anylonger')
def then_i_can_not_approve_attachment_anylonger(step):
    assert False, 'This step must be implemented'
@step(u'Then I can download the attachment')
def then_i_can_download_the_attachment(step):
    assert False, 'This step must be implemented'
@step(u'After I reach the limited of downloading attachment')
def after_i_reach_the_limited_of_downloading_attachment(step):
    assert False, 'This step must be implemented'
@step(u'Then I can not download attachment anylonger')
def then_i_can_not_download_attachment_anylonger(step):
    assert False, 'This step must be implemented'