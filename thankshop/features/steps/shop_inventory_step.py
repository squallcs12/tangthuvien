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

@step(u'I see item "([^"]*)" in my inventory')
def i_see_that_item_in_my_inventory(step, item_name):
    items = find_all("#my_items .item")
    item_names = [item.text for item in items]
    item_names.should.contain(item_name)

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

@step(u'I click on button "([^"]*)"')
def i_click_on_button(step, button_text):
    ShortDom.button(button_text).click()

@step(u'I click on modal button "([^"]*)"')
def i_click_on_modal_button(step, button_text):
    ShortDom.button(button_text, parent=".modal").click()

@step(u'I go to my inventory page')
def i_go_to_my_inventory_page(step):
    visit_by_view_name("thankshop_user_inventory", kwargs={'username': 'me'})

@step(u'I click on item "([^"]*)" in inventory')
def i_click_on_item_group1_in_inventory(step, item_name):
    item_id = Item.objects.get(name=item_name).id
    find("#my_items .item[item-id='%s']" % item_id).click()

@step(u'I see the item "([^"]*)" information')
def i_see_the_item_group1_information(step, item):
    until(lambda: find("#item_information").is_displayed().should.be.true)
    # wait for angularjs rendering
    until(lambda: find("#item_information .title").text.should.equal(item))
    find("#item_information .description").text.should.equal(item)
    find("#item_information img.image").get_attribute("src").should_not.equal("")

