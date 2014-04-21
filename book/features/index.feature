Feature: Book App :: Book listing page

    Scenario: User visit book list
        Given there are "40" books exist in the system
        And there are categories exist in the system:
            | category   |
            | category-0 |
            | category-1 |
            | category-2 |
            | category-3 |
        And each book belong to some of categories
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
        And the loading animation finished
        Then I see the url was changed
        And I see only books in that category were listed
        When I choose one more book category
        And the loading animation finished
        Then I see only books in those categories was listed
        And I see the books still there after reload the page
        When I click browser back button
        Then I see the previous books was listed
        When I clear selected book categories
        And the loading animation finished
        Then I see all the books were listed

	Scenario: List book by author
		Given author "author-1" has "2" books
		Given author "author-2" has "2" books
		When I visit book index page
		And I click on a book name
		And I click on the author name
		Then I should see "2" books in list
		And all books are written by the the clicked author
