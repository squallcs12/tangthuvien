Feature: Books page
	
	Scenario: Read book as user
		Given I was a logged-in user
		When I visit book index page
		And I click on a book
		When I choose a random chapter from selection box
		When I visit book index page
		And I click on the previous book
		And I see the last random chapter
		And I see chapter thank count
		And I can thank the poster for this chapter
		When I thank the poster for this chapter
		Then I see the chapter thank was increased
		And I can not thank the poster anymore
		When I reload the page
		Then I still see thank number not change after increasing
		And I can not thank the poster