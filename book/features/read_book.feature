Feature: Books page
	
	Scenario: Read book as guest
		Given I was a non-logged-in user
		When I visit book index page
		And I click on a book
		Then I see the book title and description
		And I see the author name and information
		And I see the first chapter
		When I go to next chapter
		Then I see the book title and description
		And I see the author name and information
		And I see the second chapter
		When I choose a random chapter from selection box
		Then I see the book title and description
		And I see the author name and information
		And I see a random chapter
		When I go to last chapter
		Then I see the book title and description
		And I see the last chapter
		
		
	Scenario: Read book as user
		Given I was a logged-in user
		When I visit book index page
		And I click on a book
		When I choose a random chapter from selection box
		When I visit book index page
		And I click on the previous book
		And I see the last random chapter