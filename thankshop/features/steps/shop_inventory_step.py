'''
Created on Dec 4, 2013

@author: eastagile
'''
from lettuce_setup.function import *
from thankshop.models.item import Item

@step(u'I go to the shop page')
def i_go_to_the_shop_page(step):
    visit_by_view_name('thankshop_shop_homepage')

@step(u'I see list of items')
def i_see_list_of_items(step):
    find("#thankshop #items")

@step(u'I see a "([^"]*)" modal with text "([^"]*)"')
def i_see_a_modal_with_text(step, modal_id, text):
    until(lambda: find("#%s" % modal_id).is_displayed().should.be.true)
    until(lambda: find("#%s" % modal_id).text.should.contain(text))

@step(u'I see that item in my inventory')
def i_see_that_item_in_my_inventory(step):
    items = find_all("#my_items .item")
    item_ids = [item.get_attribute("item-id") for item in items]
    item_ids.should.contain(world.shop_item_id)

@step(u'I click on item in inventory')
def i_click_on_item_in_inventory(step):
    item = find("#my_items .item[item-id='%s']" % world.shop_item_id)
    item.find(".view").click()

@step(u'there is a list of shop item:')
def there_is_a_list_of_shop_item(step):
    for row in step.hashes:
        item = Item()
        item.price = int(row['price'])
        item.long_description = item.short_description = item.name = row['name']
        item.stocks = 1
        item.save()

@step(u'I click on modal "([^"]*)"')
def i_click_on_modal(step, text):
    i_click_on(step, text, parent=".modal")

@step(u'I see a popup notification "([^"]*)"')
def i_see_a_popup_notification(step, text):
    find("#popup-notification").text.should.contain(text)

@step(u'I go to my inventory page')
def i_go_to_my_inventory_page(step):
    visit_by_view_name("thankshop_user_inventory", kwargs={'username': 'me'})

@step(u'I click on item "([^"]*)" in inventory')
def i_click_on_item_group1_in_inventory(step, group1):
    item = find("#my_items .item[item-id='%s']" % world.shop_item_id)
    item.find(".view").click()

@step(u'I see the item "([^"]*)" information')
def i_see_the_item_group1_information(step, item):
    until(lambda: find("#item_information").is_displayed().should.be.true)
    find("#item_information .title").text.should_not.equal(item)
    find("#item_information .description").text.should_not.equal(item)
    find("#item_information img.image").get_attribute("src").should_not.equal("")

