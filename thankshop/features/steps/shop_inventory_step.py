'''
Created on Dec 4, 2013

@author: eastagile
'''
from lettuce_setup.function import *

@step(u'When I go to the shop page')
def when_i_go_to_the_shop_page(step):
    visit_by_view_name('thankshop_shop_homepage')

@step(u'Then I see list of items')
def then_i_see_list_of_items(step):
    find("#thankshop #items")

@step(u'When I buy an item')
def when_i_buy_an_item(step):
    world.shop_item_id = find("#thankshop #items .item").get_attribute("item-id")
    find("#thankshop #items .item .buy").click()
    find("#buy-confirmation .accept").click()

@step(u'Then I see that item in my inventory')
def then_i_see_that_item_in_my_inventory(step):
    visit_by_view_name("thankshop_user_inventory", kwargs={'username': 'me'})
    items = find_all("#my_items .item")
    item_ids = [item.get_attribute("item-id") for item in items]
    item_ids.should.contain(world.shop_item_id)

@step(u'When I click on item in inventory')
def when_i_click_on_item_in_inventory(step):
    item = find("#my_items .item[item-id='%s']" % world.shop_item_id)
    item.find(".view").click()

@step(u'Then I see the item information')
def then_i_see_the_item_information(step):
    until(lambda: find("#item_information").is_displayed().should.be.true)
    find("#item_information .title").text.should_not.equal("")
    find("#item_information .description").text.should_not.equal("")
    find("#item_information img.image").get_attribute("src").should_not.equal("")

