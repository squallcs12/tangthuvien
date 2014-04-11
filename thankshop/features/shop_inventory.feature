Feature: As a poster
    I want to spend my thanked points
    To buy things

    Scenario: Inventory Shopping
        Given I was a logged-in user
        And there is a list of shop item:
        	| name   | price |
        	| item 0 | 100   |
        	| item 1 | 200   |
        	| item 2 | 300   |
        	| item 3 | 400   |
        And I has thanked points
        When I go to the shop page
        Then I see list of items
        When I click on button "Buy for 100"
        Then I see a "buy-confirmation" modal with text "item 0"
        When I click on modal button "Buy for 100"
        Then I should see the popup notification "Item item 0 was added to your inventory."
        When I go to my inventory page
        Then I see item "item 0" in my inventory
        When I click on item "item 0" in inventory
        Then I see the item "item 0" information