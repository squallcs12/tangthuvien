'''
Created on Dec 4, 2013

@author: eastagile
'''
from lettuce_setup.function import *
from thankshop import models
from book.features.factories.book_factory import BookFactory
from book.features.factories.chapter_factory import ChapterFactory
from book.features.steps.thank_chapter_steps import i_thank_the_poster_for_this_chapter
from book.models.book_model import Book
from book.features.steps.upload_book_attachments_steps import read_book_by_id
from book.models.language_model import Language
from book.features.factories.language_factory import LanguageFactory
from thankshop.models.package import Package


world.thank_points = 0

def check_thank_point(points, user_number=1):
    thank_obj = models.ThankPoint.objects.get(user=default_user(user_number))
    thank_obj.thank_points.should.equal(points)

@step(u'I log into the website for the first time in a day')
def i_log_into_the_website_for_the_first_time_in_a_day(step):
    for row in models.UserDailyLoginHistory.objects.all():
        row.delete()
    given_i_was_a_logged_in_user(step)

@step(u'I receive a number of thank points')
def i_receive_a_number_of_thank_points(step):
    world.thank_points += settings.THANKSHOP_DAILY_LOGIN_THANK_POINTS
    check_thank_point(world.thank_points)

@step(u'I re-login again')
def i_re_login_again(step):
    logout_current_user()
    given_i_was_a_logged_in_user(step)

@step(u'I do not receive any thank points')
def i_do_not_receive_any_thank_points(step):
    check_thank_point(world.thank_points)

@step(u'I do not log into website in the next day')
def i_do_not_log_into_website_in_the_next_day(step):
    logout_current_user()
    login_hostory = models.UserDailyLoginHistory.objects.get(user=default_user)
    login_hostory.date -= datetime.timedelta(days=2)
    login_hostory.save()

@step(u'I see my thank points was decreased')
def i_see_my_thank_points_was_decreased(step):
    world.thank_points += settings.THANKSHOP_DAILY_LOGIN_THANK_POINTS
    world.thank_points += settings.THANKSHOP_DAILY_NOT_LOGIN_THANK_POINTS
    given_i_was_a_logged_in_user(step)
    db_commit()
    check_thank_point(world.thank_points)

@step(u'I thank a poster for a chapter')
def i_thank_a_poster_for_a_chapter(step, book_index= -1):
    if book_index == -1:
        if not hasattr(world, 'thankshop_book_index'):
            world.thankshop_book_index = 0
        book_index = world.thankshop_book_index
        world.thankshop_book_index += 1

    try:
        language = Language.objects.all()[0]
    except IndexError:
        language = LanguageFactory()
        language.save()

    try:
        book = Book.objects.all()[book_index]
    except IndexError:
        book = BookFactory()
        book.save()
        book.languages.add(language)
        book.save()

    try:
        chapter = book.chapter_set.all()[0]
    except IndexError:
        chapter = ChapterFactory()
        chapter.number = 1
        chapter.book = book
        chapter.user = default_user(2)
        chapter.language = language
        chapter.save()
    read_book_by_id(book.id)
    if len(find_all("#read_book")):
        find("#read_book").click()
    thank_obj = models.ThankPoint.objects.get(user=default_user())
    world.thank_points = thank_obj.thank_points
    i_thank_the_poster_for_this_chapter(step)

@step(u'I see my thank points was spent')
def then_i_see_my_thank_points_was_spent(step):
    world.thank_points += settings.THANKSHOP_THANK_POINTS_COST
    check_thank_point(world.thank_points)

@step(u'And poster thanked points was increased by half of those points')
def and_poster_thanked_points_was_increased_by_half_of_those_points(step):
    thank_obj = models.ThankPoint.objects.get(user=default_user(2))
    thank_obj.thanked_points.should.equal(
        settings.THANKSHOP_THANK_POINTS_COST * settings.THANKSHOP_THANK_POINTS_PERCENT * -1
    )

@step(u'I use all my thank points')
def i_use_all_my_thank_points(step):
    thank_obj = models.ThankPoint.objects.get(user=default_user())
    thank_obj.thank_points = 0
    thank_obj.save()

@step(u'I can not thank anylonger')
def i_can_not_thank_anylonger(step):
    i_thank_a_poster_for_a_chapter(step)
    until(lambda: find("#popup-notitication").is_displayed().should.be.true)
    find("#popup-notitication .modal-body").text.should\
        .contain(trans(u"You need at least %(number)d thank points to do thank") % {
                'number':-settings.THANKSHOP_THANK_POINTS_COST
            })

@step(u'I can not give any thank in a short time')
def i_can_not_give_any_thank_in_a_short_time(step):
    i_thank_a_poster_for_a_chapter(step)
    until(lambda: find("#popup-notitication").is_displayed().should.be.true)
    find("#popup-notitication .modal-body").text.should.contain(trans(u"You can not thank in next"))

@step(u'I has thanked points')
def given_i_has_thanked_points(step):
    try:
        thank_obj = models.ThankPoint.objects.get(user=default_user())
    except ObjectDoesNotExist:
        thank_obj = models.ThankPoint(user=default_user())
    thank_obj.thanked_points = 1000
    thank_obj.save()

@step(u'I go to the buy thank points page')
def i_go_to_the_buy_thank_points_page(step):
    visit_by_view_name('thankshop_thank_point_shop')

@step(u'I see a list of thank points packages')
def i_see_a_list_of_thank_points_packages(step):
    find("#thankshop #packages")

@step(u'I buy a package of "([^"]*)" thank points')
def i_buy_a_package_of_group1_thank_points(step, points):
    world.current_thank_points = models.ThankPoint.objects.get(user=default_user()).thank_points
    packages = [package for package in find_all("#thankshop #packages .package")]
    for package in packages:
        if package.find(".points").text == points:
            package.find(".buy").click()
            break
    world.thank_points_package_points = int(points)

@step(u'I enter my paypal login information')
def i_enter_my_paypal_login_information(step):
    find("#billingModule .panel").click()  # pay with paypal account
    find("#login_email").fillin(settings.TEST_EMAIL)
    find("#login_password").fillin(settings.TEST_PASSWORD)
    find("#submitLogin").click()

@step(u'I approve the buying process')
def i_approve_the_buying_process(step):
    until(lambda: find("#continue_abovefold").click())

@step(u'I receive an amount of thank points to spend')
def i_receive_an_amount_of_thank_points_to_spend(step):
    thank_points = world.current_thank_points + world.thank_points_package_points
    until(lambda: models.ThankPoint.objects.get(user=default_user()).thank_points.should.equal(thank_points))

@step(u'there is a list of thankpoint package:')
def there_is_a_list_of_thankpoint_package(step):
    for row in step.hashes:
        package = Package()
        package.name = row['name']
        package.price = int(row['price'])
        package.points = int(row['points'])
        package.sku = row['name']
        package.save()

@step(u'I was redirected to paypal checkout')
def i_was_redirected_to_paypal_checkout(step):
    until(lambda: browser().current_url.should.contain("paypal.com"))
