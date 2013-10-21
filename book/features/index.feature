Feature: Book App :: Book listing page

	Scenario: User visit book list
		When I visit book index page
		Then I see list of books
		And I was at the first page of listing
		When I go to the next page
		Then I see list of books
		And those books difference from the first page
		And I was at the second page of listing
		When I go to the last page
		Then I see list of books
		And I was at the last page of listing
		And those books difference from the other pages
		And I was at the last page of listing
		When I choose a book category
		Then I see only books in that category were listed
		When I choose one more book category
		Then I see only books in those categories was listed
		When I clear selected book categories
		Then I see all the books were listed

		