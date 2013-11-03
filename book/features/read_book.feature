Feature: Book App :: Book reading page

	Scenario: Read book as guest
		Given I was a non-logged-in user
		When I visit book index page
		And I click on a book
		Then I see the book rating box
		And I see the book rating result
		And I see rating book button
		And I can not rate for the book
		And I see the "Start reading" button
		When I click on the "Start reading" button
		Then I see the first chapter
		When I go to next chapter
		Then I see the second chapter
		When I choose a random chapter from selection box
		Then I see a random chapter
		When I go to last chapter
		Then I see the last chapter
		And I see chapter thank count
		And I can not thank the poster

	Scenario: Read book as user
		Given I was a logged-in user
		When I visit book index page
		And I click on a book
		Then I see the book rating box
		And I see the book rating result
		And I see rating book button
		And I can rate for the book
		And I see the book rating count is 0
		When I rate 5 star for the book
		Then I see the book rating is 5.00
		And I see the book rating count is 1
		And I can not rate for the book anylonger
		And I see the "Start reading" button
		When I click on the "Start reading" button
		And I choose a random chapter from selection box
		And I visit book index page
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
		And I see the book rating is 5.00
		And I see the book rating count is 1
		And I can not rate for the book anylonger

	Scenario: Configurate reading section
		Given I was a logged-in user
		When I read a book
		And I change the reading section font face and font size
		Then I see the configuration of readind section is applied
		When I go to next chapter
		Then I see the configuration of readind section is applied
		When I read another book
		Then I see the configuration of readind section is applied