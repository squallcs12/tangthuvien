Feature: As a poster
	I want to spend my thanked points
	To buy things

	Scenario: Inventory Shopping
		Given I was a logged-in user
		And I has thanked points
		When I go to the shop page
		Then I see list of items
		When I buy an item
		Then I see that item in my inventory
		When I click on item in inventory
		Then I see the item information