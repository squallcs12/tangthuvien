Feature: Book App :: Post new chapter

	Scenario: User post new chapter
		Given I was a logged-in user
		When I am reading a book
		And I submit a new book chapter
		Then I see new chapter was posted
		And other people can read this chapter
		And my posted chapter was increased
		
	Scenario: User edit chapter
		Given I was a logged-in user
		When I am reading a book
		And I edit that chapter
		Then I see that chapter was edited
